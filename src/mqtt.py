# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import json
import mosquitto

class MQTTPublisher(object):

    def __init__(self, host, port=1883, timeout=60, topic='mqtt-publisher', client_id_prefix=None):

        self.host = host
        self.port = port
        self.timeout = timeout
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
        #print self.host, self.port, self.timeout
        self.mqttc.connect(self.host, self.port, self.timeout)
        self.mqttc.publish(self.topic + '/helo', 'hello world')

        # attach MQTT callbacks
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        #mqttc.on_message = on_message

    def close(self):
        self.mqttc.disconnect()

    def publish_real(self, topic, data):
        print 'INFO:    publishing {} {}'.format(topic, data)
        self.mqttc.publish(topic, data)

    def publish_point(self, name, value, data):
        topic = '{topic}/{network_id}/{gateway_id}/{node_id}/{name}'.format(topic=self.topic, name=name, **data)
        self.publish_real(topic, value)

    def publish_scalar(self, data, name, value):
        self.publish_point(name, value, data)

    def publish_field(self, data, fieldname):
        #print 'node_topic:', node_topic
        try:
            self.publish_point(fieldname, data[fieldname], data)
        except KeyError:
            print 'WARNING: Could not publish field "{}"'.format(fieldname)

    def publish_json(self, data, name, value):
        #print 'node_topic:', node_topic
        self.publish_point(name, json.dumps(value), data)


    # MQTT callbacks
    def on_connect(self, mosq, obj, rc):
        if rc == 0:
            print("MQTT: Connected successfully.")
        else:
            raise Exception

    def on_disconnect(self, mosq, obj, rc):
        print("MQTT: Disconnected successfully.")

    def on_publish(self, mosq, obj, mid):
        #print("Message "+str(mid)+" published.")
        pass

    def on_subscribe(self, mosq, obj, mid, qos_list):
        print("MQTT: Subscribe with mid "+str(mid)+" received.")

    def on_unsubscribe(self, mosq, obj, mid):
        print("MQTT: Unsubscribe with mid "+str(mid)+" received.")

    def on_message(self, mosq, obj, msg):
        print("MQTT: Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload)



class BERadioMQTTPublisher(MQTTPublisher):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('topic', 'beradio')
        return MQTTPublisher.__init__(self, *args, **kwargs)

    def publish_flexible(self, data, do_json=True, bencode_raw=None):

        # publish to different topics
        self.publish_field(data, 'temp1')
        self.publish_field(data, 'temp2')
        self.publish_field(data, 'temp3')
        self.publish_field(data, 'temp4')
        self.publish_field(data, 'hum1')
        self.publish_field(data, 'hum2')
        self.publish_field(data, 'wght1')

        # publish en-bloc
        if do_json:
            self.publish_json(data, 'message-json', data)
        if bencode_raw:
            self.publish_scalar(data, 'message-bencode', bencode_raw)
