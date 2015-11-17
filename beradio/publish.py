# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import random
from mqtt import BERadioMQTTAdapter
import logging
from beradio.network import protocol_factory

"""
Read data in Bencode format from command line, decode and publish via MQTT.

Synopsis::

  # send given Bencode payload
  python publish.py 192.168.59.103 li999ei99ei1ei2218ei2318ei2462ei2250ee

  # send random values
  python publish.py 192.168.59.103 random

"""

logger = logging.getLogger(__name__)

class DataToMQTT(object):

    def __init__(self, mqtt_broker, mqtt_topic='hiveeyes', protocol=2):
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic
        self.protocol_class = protocol_factory(protocol)

    def setup(self):
        try:
            logger.info('Connecting to MQTT broker "{}"'.format(self.mqtt_broker))
            self.mqtt = BERadioMQTTAdapter(self.mqtt_broker, topic=self.mqtt_topic)
        except:
            logger.error('Failed to connect to MQTT broker "{}"'.format(self.mqtt_broker))
            raise

        return self

    def publish(self, payload):

        if payload == 'random':
            if self.protocol_class.VERSION == 1:
                data = [
                    '999', '99', '2',
                    scale_100(random_temp()), scale_100(random_temp()), scale_100(random_temp()), scale_100(random_temp()),
                ]
            elif self.protocol_class.VERSION == 2:
                data = {
                    '#': '999',
                    '_': 'h1',
                    't': [scale_100(random_temp()), scale_100(random_temp()), scale_100(random_temp()), scale_100(random_temp())],
                    'h': [scale_100(random_hum()), scale_100(random_hum())],
                    'w': scale_100(random_weight())}
            payload = self.protocol_class.encode_ether(data)
            logger.info('random payload: {}'.format(payload))

        # decode wire format
        data = self.protocol_class.decode(payload)
        logger.debug('data: {}'.format(data))

        if self.protocol_class.VERSION == 1:
            data = self.protocol_class.to_v2(data)

        # publish to MQTT
        self.mqtt.publish_flexible(data, bencode_raw=payload)

    def __del__(self):
        if hasattr(self, 'mqtt'):
            logger.info('Disconnecting from MQTT broker')
            self.mqtt.close()


def random_temp():
    return round(random.uniform(7, 26), 2)

def random_hum():
    return round(random.uniform(3, 11), 2)

def random_weight():
    return round(random.uniform(100, 130), 2)

def scale_100(temp):
    return int(temp * 100)


if __name__ == '__main__':
    DataToMQTT(mqtt_broker=sys.argv[1], protocol=1).setup().publish(sys.argv[2])
