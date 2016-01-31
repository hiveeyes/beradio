# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import logging
import json
import mosquitto

logger = logging.getLogger(__name__)

class MQTTAdapter(object):

    def __init__(self, host, port=1883, keepalive=60, topic='beradio', client_id_prefix=None):

        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.topic = topic

        self.client_id_prefix = client_id_prefix or topic

        # create a mqtt client
        # TODO: maybe use UUIDs here?
        pid = os.getpid()
        client_id = '{}:{}'.format(self.client_id_prefix, str(pid))
        self.mqttc = mosquitto.Mosquitto(client_id)
        self.connect()

    def connect(self):

        # connect to broker
        self.mqttc.connect(self.host, self.port, self.keepalive)
        self.mqttc.publish(self.topic + '/helo', 'hello world')

        # attach MQTT callbacks
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        self.mqttc.on_message = self.on_message

    def close(self):
        self.mqttc.disconnect()

    def publish(self, topic, data):
        logger.debug('publishing {} {}'.format(topic, data))
        return self.mqttc.publish(topic, data)

    def subscribe(self, topic):
        logger.info('subscribe: {}'.format(topic))
        return self.mqttc.subscribe(topic)

    # MQTT callbacks
    def on_connect(self, mosq, obj, rc):
        if rc == 0:
            logger.info("Connected successfully")
        else:
            raise Exception

    def on_disconnect(self, mosq, obj, rc):
        logger.info("Disconnected successfully")

    def on_publish(self, mosq, obj, mid):
        #logger.info("Message "+str(mid)+" published.")
        pass

    def on_subscribe(self, mosq, obj, mid, qos_list):
        logger.info("Subscribe with mid "+str(mid)+" received")

    def on_unsubscribe(self, mosq, obj, mid):
        logger.info("Unsubscribe with mid "+str(mid)+" received")

    def on_message(self, mosq, obj, msg):
        logger.info("Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload)


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
            publisher.json('message-json', message['data'])
        if bencode_raw:
            publisher.scalar('message-beradio', bencode_raw)

    def publish_json(self, message):
        publisher = BERadioMQTTPublisher(self, self.topic, message)
        publisher.json('message-json', message['data'])

    def publish_value(self, message, name, value):
        publisher = BERadioMQTTPublisher(self, self.topic, message)
        publisher.scalar('measure/{}'.format(name), value)

    def subscribe(self, subtopic=None):
        topic = self.topic
        if subtopic:
            topic += '/' + subtopic
        return MQTTAdapter.subscribe(self, topic)
