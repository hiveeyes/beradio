# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <richard@hiveeyes.org>
# (c) 2015-2018 Andreas Motl <andreas@hiveeyes.org>
import os
import json
import logging
from urlparse import urlsplit
from collections import OrderedDict

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class MQTTAdapter(object):

    # The value of rc indicates success or not:
    RC_STATUS_MAP = {
        0: 'Connection successful',
        1: 'Connection refused - incorrect protocol version',
        2: 'Connection refused - invalid client identifier',
        3: 'Connection refused - server unavailable',
        4: 'Connection refused - bad username or password',
        5: 'Connection refused - not authorised',
        # 6 - 255: Currently unused.
    }

    def __init__(self, uri, keepalive=60, topic='beradio', client_id_prefix=None):

        address = urlsplit(uri)
        self.host       = address.hostname
        self.port       = address.port or 1883
        self.username   = address.username
        self.password   = address.password

        self.keepalive = keepalive
        self.topic = topic

        self.client_id_prefix = client_id_prefix or topic

        self.connect()

    def connect(self):

        # Create a MQTT client object
        # TODO: maybe use UUIDs here?
        pid = os.getpid()
        client_id = '{}:{}'.format(self.client_id_prefix, str(pid))
        self.mqttc = mqtt.Client(client_id=client_id, clean_session=True, userdata={'gateway': True})

        # Optionally add authentication into the mix
        if self.username:
            self.mqttc.username_pw_set(self.username, self.password)

        # Connect to broker
        logger.info('Connecting to MQTT broker with '
                    'host={}, port={}, keepalive={}'.format(self.host, self.port, self.keepalive))
        self.mqttc.connect(self.host, self.port, self.keepalive)
        #self.mqttc.publish(self.topic + '/helo', 'hello world')

        # Attach MQTT callbacks
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        self.mqttc.on_message = self.on_message

    def get_status(self):
        status = OrderedDict()
        status['host'] = self.host
        status['port'] = self.port
        return status

    def close(self):
        self.mqttc.disconnect()

    def publish(self, topic, data):
        logger.debug('Publishing to topic {}. data={}'.format(topic, data))
        return self.mqttc.publish(topic, data)

    def subscribe(self, topic):
        logger.info('Subscribing to topic {}'.format(topic))
        return self.mqttc.subscribe(topic)

    # MQTT callbacks
    def on_connect(self, client, userdata, flags, rc):

        # Get status information
        status = self.get_status()
        status['userdata'] = userdata
        status['flags'] = flags
        status['rc'] = rc
        status['rc_message'] = self.RC_STATUS_MAP.get(rc)

        if rc == 0:
            status['status'] = 'ok'
            logger.info('Connection to MQTT broker succeeded: {}'.format(json.dumps(status)))
        else:
            status['status'] = 'error'
            logger.error('Connection to MQTT broker failed: {}'.format(json.dumps(status)))

    def on_disconnect(self, client, userdata, *args):
        logger.info('Disconnection from MQTT broker succeeded')

    def on_publish(self, client, userdata, mid):
        #logger.info("Message " + str(mid) + " published.")
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info("Subscribe with mid " + str(mid) + " received")

    def on_unsubscribe(self, client, userdata, mid):
        logger.info("Unsubscribe with mid " + str(mid) + " received")

    def on_message(self, client, userdata, message):
        logger.info(u'Message received on topic {} with QoS {} and payload {}'.format(
            message.topic, str(message.qos), message.payload))


class MQTTPublisher(object):

    topic_template = None

    def __init__(self, mqtt_publisher, realm, message):
        self.mqtt = mqtt_publisher
        self.realm = realm
        self.message = message

    def publish(self, name, value):
        topic = self.compute_topic(name=name, metadata=self.message['meta'])
        self.mqtt.publish(topic, value)

    def compute_topic(self, name, metadata):
        tplvars = {}
        tplvars.update({'name': name})
        tplvars.update({'realm': self.realm})
        tplvars.update(metadata)
        topic = self.topic_template.format(**tplvars)
        #logger.info('topic: {}'.format(topic))
        return topic

    def scalar(self, name, value):
        self.publish(name, value)

    def field(self, fieldname):
        try:
            value = self.message['data'][fieldname]
        except KeyError:
            logger.warning('Could not find field "{}" to publish'.format(fieldname))
            return

        self.publish(fieldname, value)

    def all_fields(self):
        for key in self.message['data'].keys():
            self.field(key)

    def json(self, name, value):
        self.publish(name, json.dumps(value))


class BERadioMQTTPublisher(MQTTPublisher):
    topic_template = u'{realm}/{network}/{gateway}/{node}/{name}'

class BERadioMQTTAdapter(MQTTAdapter):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('topic', 'beradio')
        return MQTTAdapter.__init__(self, *args, **kwargs)

    def publish_flexible(self, message, do_json=True, bencode_raw=None):

        publisher = BERadioMQTTPublisher(self, self.topic, message)

        # publish all data values to discrete topics
        publisher.all_fields()

        # 2015-11-14: add nanosecond timestamp to json message to improve acquisition precision
        if 'time' in message['meta']:
            message['data']['time'] = message['meta']['time']

        # publish en-bloc
        if do_json:
            publisher.json('data.json', message['data'])
        if bencode_raw:
            publisher.scalar('data.beradio', bencode_raw)

    def publish_json(self, message):
        publisher = BERadioMQTTPublisher(self, self.topic, message)
        publisher.json('data.json', message['data'])

    def publish_value(self, message, name, value):
        publisher = BERadioMQTTPublisher(self, self.topic, message)
        publisher.scalar('measure/{}'.format(name), value)

    def subscribe(self, subtopic=None):
        topic = self.topic
        if subtopic:
            topic += '/' + subtopic
        return MQTTAdapter.subscribe(self, topic)
