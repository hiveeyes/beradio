#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import random
from beradio.protocol import get_protocol_class
from mqtt import BERadioMQTTPublisher

"""
Read data in Bencode format from command line, decode and publish via MQTT.

Synopsis::

  # send given Bencode payload
  python publish.py 192.168.59.103 li999ei99ei1ei2218ei2318ei2462ei2250ee

  # send random values
  python publish.py 192.168.59.103 random

"""

class DataToMQTT(object):

    def __init__(self, mqtt_broker, mqtt_topic='hiveeyes', protocol=2):
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic
        self.protocol_class = get_protocol_class(protocol)

    def setup(self):
        try:
            print 'INFO:  Connecting to MQTT broker "{}"'.format(self.mqtt_broker)
            self.mqtt = BERadioMQTTPublisher(self.mqtt_broker, timeout=0, topic=self.mqtt_topic)
        except:
            print 'ERROR: Failed to connect to MQTT broker "{}"'.format(self.mqtt_broker)
            raise SystemExit

        return self

    def publish(self, payload):

        if payload == 'random':
            if self.protocol_class.VERSION == 1:
                data = [
                    '999', '99', '1',
                    scale_100(random_temp()), scale_100(random_temp()), scale_100(random_temp()), scale_100(random_temp()),
                ]
            elif self.protocol_class.VERSION == 2:
                data = {
                    't': [scale_100(random_temp()), scale_100(random_temp()), scale_100(random_temp()), scale_100(random_temp())],
                    'h': [scale_100(random_hum()), scale_100(random_hum())],
                    'w': scale_100(random_weight())}
            payload = self.protocol_class.encode_ether(data)
            print 'random payload:', payload

        # decode wire format
        data = self.protocol_class.decode(payload)
        #print 'data:', data

        # publish to MQTT
        self.mqtt.publish_flexible(data, bencode_raw=payload)


    def __del__(self):
        if hasattr(self, 'mqtt'):
            print 'INFO:   Disconnecting from MQTT broker'
            self.mqtt.close()


def random_temp():
    return round(random.uniform(7, 26), 2)

def random_hum():
    return round(random.uniform(3, 11), 2)

def random_weight():
    return round(random.uniform(40, 160), 2)

def scale_100(temp):
    return int(temp * 100)


if __name__ == '__main__':
    DataToMQTT(mqtt_broker=sys.argv[1], protocol=1).setup().publish(sys.argv[2])
