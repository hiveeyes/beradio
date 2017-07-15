# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import time
import json
import random
import logging
try:
    from pprint import pprint
except ImportError:
    from pprint import pformat
    def pprint(x):
        print(pformat(x))
from message import BERadioMessage
from .network import protocol_factory
from .mqtt import BERadioMQTTAdapter
from .util import math_func

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

        # use mqtt.loop_forever() in a separate thread, this will handle
        # automatic reconnecting if connection to broker got lost
        self.mqtt.mqttc.loop_start()

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
            self.publish_real(payload)

        elif payload.startswith('func:'):

            func_name = payload.replace('func:', '')

            x = 1.0

            def apply_func(func_name, x, times):
                shifting_factor = 3
                for i in range(times):
                    y = math_func(func_name, x + i * 3)
                    yield y

            #interval = 0
            #interval = 0.01
            interval = 0.2

            logger.info('Starting publishing loop with interval={}'.format(interval))
            while True:
                x += 1

                message = BERadioMessage(999, profile='h1')
                message.temperature(*apply_func(func_name, x, 4))
                message.humidity(*apply_func(func_name, x, 2))
                message.weight(math_func(func_name, x))
                pprint(message)

                # publish to MQTT
                self.publish_real(message.encode())

                time.sleep(interval)

        elif payload.startswith('json:'):
            json_payload = payload.replace('json:', '')
            data = json.loads(json_payload)

            node_id = data.get('node', '999')

            message = {
                'meta': {
                    'protocol': 'mqttkit1',
                    'network': str(self.protocol_class.network_id),
                    'gateway': str(self.protocol_class.gateway_id),
                    'node': node_id,
                    },
                'data': data,
                }

            self.mqtt.publish_json(message)

        elif payload.startswith('value:'):
            json_payload = payload.replace('value:', '')
            data = json.loads(json_payload)

            first = data.items()[0]
            name = first[0]
            value = first[1]

            #print name, value

            message = {
                'meta': {
                    'protocol': 'mqttkit1',
                    'network': str(self.protocol_class.network_id),
                    'gateway': str(self.protocol_class.gateway_id),
                    'node': 999,
                    },
                'data': data,
                }

            self.mqtt.publish_value(message, name, value)


        else:
            self.publish_real(payload)


        self.mqtt.mqttc.loop_stop()


    def publish_real(self, payload):

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
