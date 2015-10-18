# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import json
import mosquitto

class MQTTPublisher(object):

    def __init__(self, host, port=1883, timeout=60, topic='serial-to-mqtt'):

        self.host = host
        self.port = port
        self.timeout = timeout
        self.topic = topic

        # create a mqtt client
        mypid = os.getpid()
        client_uniq = "serial-to-mqtt:" + str(mypid)
        self.mqttc = mosquitto.Mosquitto(client_uniq)
        self.connect()

    def connect(self):

        # connect to broker
        #print self.host, self.port, self.timeout
        self.mqttc.connect(self.host, self.port, self.timeout)
        self.mqttc.publish(self.topic + '/helo', 'hello world')

        # attach MQTT callbacks
        self.mqttc.on_connect = on_connect
        self.mqttc.on_disconnect = on_disconnect
        self.mqttc.on_publish = on_publish
        self.mqttc.on_subscribe = on_subscribe
        self.mqttc.on_unsubscribe = on_unsubscribe
        #mqttc.on_message = on_message

    def close(self):
        self.mqttc.disconnect()

    def publish(self, topic, data):
        print 'publish:', topic, data
        self.mqttc.publish(topic, data)

    def publish_point(self, name, value, data):
        topic = '{topic}/{network_id}/{gateway_id}/{node_id}/{name}'.format(topic=self.topic, name=name, **data)
        self.publish(topic, value)

    def publish_scalar(self, data, name, value):
        self.publish_point(name, value, data)

    def publish_field(self, data, fieldname):
        #print 'node_topic:', node_topic
        self.publish_point(fieldname, data[fieldname], data)

    def publish_json(self, data, name, value):
        #print 'node_topic:', node_topic
        self.publish_point(name, json.dumps(value), data)


# MQTT callbacks
def on_connect(mosq, obj, rc):
    if rc == 0:
        print("MQTT: Connected successfully.")
    else:
        raise Exception

def on_disconnect(mosq, obj, rc):
    print("MQTT: Disconnected successfully.")

def on_publish(mosq, obj, mid):
    #print("Message "+str(mid)+" published.")
    pass

def on_subscribe(mosq, obj, mid, qos_list):
    print("MQTT: Subscribe with mid "+str(mid)+" received.")

def on_unsubscribe(mosq, obj, mid):
    print("MQTT: Unsubscribe with mid "+str(mid)+" received.")

def on_message(mosq, obj, msg):
    print("MQTT: Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload)
