# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <richard@hiveeyes.org>
# (c) 2015-2018 Andreas Motl <andreas@hiveeyes.org>
import json
import logging
import os
import threading
import time
from collections import OrderedDict
from copy import deepcopy
from datetime import datetime
from urllib.parse import urlsplit

import paho.mqtt.client as mqtt

from beradio import program_name
from beradio.network import protocol_factory
from beradio.util import get_hostname

logger = logging.getLogger(__name__)


class MQTTAdapter(object):

    # The value of rc indicates success or not:
    RC_STATUS_MAP = {
        0: "Connection successful",
        1: "Connection refused - incorrect protocol version",
        2: "Connection refused - invalid client identifier",
        3: "Connection refused - server unavailable",
        4: "Connection refused - bad username or password",
        5: "Connection refused - not authorised",
        # 6 - 255: Currently unused.
    }

    def __init__(self, uri, keepalive=60, topic=None, enable_heartbeat=False):

        # Decode MQTT connection URL, e.g.
        # mqtt://test@example.org:12345@mqtt.example.org/testdrive/
        address = urlsplit(uri)

        # Propagate components of connection string
        self.host = address.hostname
        self.port = address.port or 1883
        self.username = address.username
        self.password = address.password
        self.keepalive = keepalive

        # Derive MQTT topic from connection URL
        # TODO: Revisit and check whether the "topic" parameter still makes sense at all?
        self.topic = topic or address.path.lstrip("/").rstrip("/")

        # Whether to send out high-level ping probes
        self.enable_heartbeat = enable_heartbeat

        # Compute MQTT client id
        program = program_name()
        hostname = get_hostname()
        pid = os.getpid()
        self.client_id = "{program}:{hostname}:{pid}".format(program=program, hostname=hostname, pid=pid)

        # Attempt to connect to MQTT broker
        self.connect()

    def connect(self):

        # Define userdata which will be attached to each message
        userdata = {"gateway": True}

        # Create a MQTT client object
        self.mqttc = mqtt.Client(client_id=self.client_id, clean_session=True, userdata=userdata)

        # Optionally add authentication into the mix
        if self.username:
            self.mqttc.username_pw_set(self.username, self.password)

        # Connect to broker
        logger.info(
            "Connecting to MQTT broker with "
            "host={}, port={}, keepalive={}".format(self.host, self.port, self.keepalive)
        )
        self.mqttc.connect(self.host, self.port, self.keepalive)

        # Attach MQTT callbacks
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        self.mqttc.on_message = self.on_message

    def get_status(self):
        status = OrderedDict()
        status["host"] = self.host
        status["port"] = self.port
        status["username"] = self.username
        return status

    def close(self):
        logger.info("Closing connection to MQTT broker")
        if self.enable_heartbeat:
            self.set_offline()
            time.sleep(0.25)
        self.mqttc.disconnect()

    def publish(self, topic, data, retain=False):
        logger.debug("Publishing to topic {}: data={}".format(topic, data))
        return self.mqttc.publish(topic, data, retain=retain)

    def subscribe(self, topic):
        logger.info("Subscribing to topic {}".format(topic))
        return self.mqttc.subscribe(topic)

    # MQTT callbacks
    def on_connect(self, client, userdata, flags, rc):

        # Get status information
        status = self.get_status()
        status["userdata"] = userdata
        status["flags"] = flags
        status["rc"] = rc
        status["rc_message"] = self.RC_STATUS_MAP.get(rc)

        if rc == 0:
            status["status"] = "ok"
            logger.info("Connection to MQTT broker succeeded: {}".format(json.dumps(status)))

            # Publish ping/alive message
            if self.enable_heartbeat:
                self.publish_ping()

        else:
            status["status"] = "error"
            logger.error("Connection to MQTT broker failed: {}".format(json.dumps(status)))

    def on_disconnect(self, client, userdata, *args):
        logger.info("Disconnection from MQTT broker succeeded")

    def on_publish(self, client, userdata, mid):
        # logger.info("Message " + str(mid) + " published.")
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info("Subscribe with mid " + str(mid) + " received")

    def on_unsubscribe(self, client, userdata, mid):
        logger.info("Unsubscribe with mid " + str(mid) + " received")

    def on_message(self, client, userdata, message):
        logger.info(
            "Message received on topic {} with QoS {} and payload {}".format(
                message.topic, str(message.qos), message.payload
            )
        )

    def publish_ping(self):
        raise NotImplementedError()

    def set_offline(self):
        raise NotImplementedError()


class MQTTPublisher(object):

    topic_template = None

    def __init__(self, mqtt_adapter, realm, message, retain=False):
        self.mqtt = mqtt_adapter
        self.realm = realm or "default"
        self.message = message
        self.retain = retain

    def publish(self, name, value):
        topic = self.compute_topic(name=name, metadata=self.message["meta"])
        self.mqtt.publish(topic, value, retain=self.retain)

    def compute_topic(self, name, metadata):
        tplvars = {}
        tplvars.update({"name": name})
        tplvars.update({"realm": self.realm})
        tplvars.update(metadata)
        topic = self.topic_template.format(**tplvars)
        # logger.info('topic: {}'.format(topic))
        return topic

    def scalar(self, name, value):
        self.publish(name, value)

    def field(self, fieldname):
        try:
            value = self.message["data"][fieldname]
        except KeyError:
            logger.warning('Could not find field "{}" to publish'.format(fieldname))
            return

        self.publish(fieldname, value)

    def all_fields(self):
        for key in self.message["data"].keys():
            self.field(key)

    def json(self, name, data):
        payload = json.dumps(data)
        self.publish(name, payload)

    def set_will(self, name, data):
        payload = json.dumps(data)
        topic = self.compute_topic(name=name, metadata=self.message["meta"])
        self.mqtt.mqttc.will_set(topic, payload=payload)


class BERadioMQTTPublisher(MQTTPublisher):
    topic_template = "{realm}/{network}/{gateway}/{node}/{name}"


class BERadioMQTTAdapter(MQTTAdapter):

    STATUS_INTERVAL = 5 * 60
    STATUS_SUFFIX = "status.json"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("enable_heartbeat", False)
        MQTTAdapter.__init__(self, *args, **kwargs)
        if self.enable_heartbeat:
            self.pinger = BERadioPinger(self, interval=self.STATUS_INTERVAL)

    def publish_flexible(self, message, do_json=True, do_discrete=False, do_bencode=False, bencode_raw=None):

        publisher = BERadioMQTTPublisher(self, self.topic, message)

        # 1. Publish data in Bencode format
        if do_bencode and bencode_raw:
            publisher.scalar("data.beradio", bencode_raw)

        # 2. Publish data in JSON format
        if do_json:

            message_block = deepcopy(message)

            # 2015-11-14: Add nanosecond timestamp to JSON message to improve acquisition precision
            if "time" in message_block["meta"]:
                message_block["data"]["time"] = message_block["meta"]["time"]

            publisher.json("data.json", message_block["data"])

        # 3. Publish all data values to discrete MQTT topics
        # TODO: Conditionally reenable again
        if do_discrete:
            publisher.all_fields()

    def publish_json(self, message):
        publisher = BERadioMQTTPublisher(self, self.topic, message)
        publisher.json("data.json", message["data"])

    def publish_value(self, message, name, value):
        publisher = BERadioMQTTPublisher(self, self.topic, message)
        publisher.scalar("data/{}".format(name), value)

    def publish_ping(self):

        logger.info("Publishing ping message")

        # Get "ping" payload
        info = self.get_status_data("online")

        # Publish to "ping.json" in the context of the designated channel
        message = protocol_factory().get_envelope(node="gateway")
        publisher = BERadioMQTTPublisher(self, self.topic, message, retain=True)
        publisher.json(self.STATUS_SUFFIX, info)

        # self.set_testament()

    def set_offline(self):

        # Get "ping" payload
        info = self.get_status_data("offline")

        # Define testament to be published to "ping.json" in the context of the designated channel
        message = protocol_factory().get_envelope(node="gateway")
        publisher = BERadioMQTTPublisher(self, self.topic, message, retain=True)
        publisher.json(self.STATUS_SUFFIX, info)

    def set_testament(self):

        print("set_testament")

        # Get "ping" payload
        info = self.get_status_data("offline")

        # Define testament to be published to "ping.json" in the context of the designated channel
        message = protocol_factory().get_envelope(node="gateway")
        publisher = BERadioMQTTPublisher(self, self.topic, message, retain=True)
        publisher.set_will(self.STATUS_SUFFIX, info)

    def get_status_data(self, status):
        """
        Define "ping" payload
        """
        info = OrderedDict()
        info["status"] = status
        info["program"] = program_name(with_version=True)
        info["date"] = datetime.utcnow().isoformat()
        return info

    def subscribe(self, subtopic=None):
        components = []
        if self.topic:
            components.append(self.topic)
        if subtopic:
            components.append(subtopic)
        topic = "/".join(components)
        return MQTTAdapter.subscribe(self, topic)


class BERadioPinger(object):
    def __init__(self, mqtt_adapter, interval=30):
        self.mqtt_adapter = mqtt_adapter
        self.interval = interval
        self.restart()

    def restart(self):
        self.timer = threading.Timer(self.interval, self.ping)
        self.timer.setDaemon(True)
        self.timer.start()

    def ping(self):
        self.mqtt_adapter.publish_ping()
        self.restart()
