# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <richard@hiveeyes.org>
# (c) 2015-2018 Andreas Motl <andreas@hiveeyes.org>
import json
import logging
import random
import sys
import time

from beradio.decoder import jobee_decode

try:
    from pprint import pprint
except ImportError:
    from pprint import pformat

    def pprint(x):
        print(pformat(x))


from .message import BERadioMessage
from .mqtt import BERadioMQTTAdapter
from .network import protocol_factory
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
    def __init__(self, mqtt_broker, mqtt_topic=None, protocol=2):
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic
        self.protocol_class = protocol_factory(protocol)

    def setup(self):
        try:
            logger.info('Connecting to MQTT broker "{}"'.format(self.mqtt_broker))
            self.mqtt = BERadioMQTTAdapter(self.mqtt_broker, topic=self.mqtt_topic, enable_heartbeat=True)
        except:  # noqa:E722
            logger.error('Failed to connect to MQTT broker "{}"'.format(self.mqtt_broker))
            raise

        return self

    def publish(self, payload):

        logger.info('Setting up publishing of "{}"'.format(payload))

        # use mqtt.loop_forever() in a separate thread, this will handle
        # automatic reconnecting if connection to broker got lost
        self.mqtt.mqttc.loop_start()

        if payload == "random":
            if self.protocol_class.VERSION == 1:
                data = [
                    "999",
                    "99",
                    "2",
                    scale_100(random_temp()),
                    scale_100(random_temp()),
                    scale_100(random_temp()),
                    scale_100(random_temp()),
                ]
            elif self.protocol_class.VERSION == 2:
                data = {
                    "#": "999",
                    "_": "h1",
                    "t": [
                        scale_100(random_temp()),
                        scale_100(random_temp()),
                        scale_100(random_temp()),
                        scale_100(random_temp()),
                    ],
                    "h": [scale_100(random_hum()), scale_100(random_hum())],
                    "w": scale_100(random_weight()),
                }
            payload = self.protocol_class.encode_ether(data)
            logger.info("Publishing random payload: {}".format(payload))
            self.publish_real(payload)

        elif payload.startswith("func:"):

            func_name = payload.replace("func:", "")

            x = 1.0

            def apply_func(func_name, x, times):
                # shifting_factor = 3
                for i in range(times):
                    y = math_func(func_name, x + i * 3)
                    yield y

            # interval = 0
            # interval = 0.01
            interval = 0.5

            logger.info("Running publishing loop with interval={}".format(interval))
            while True:
                x += 1

                message = BERadioMessage(999, profile="h1")
                message.temperature(*apply_func(func_name, x, 4))
                message.humidity(*apply_func(func_name, x, 2))
                message.weight(math_func(func_name, x))
                # pprint(message)

                if logger.level != logging.DEBUG:
                    sys.stderr.write(".")

                # publish to MQTT
                self.publish_real(message.encode())

                time.sleep(interval)

        elif payload.startswith("json:"):
            json_payload = payload.replace("json:", "")
            data = json.loads(json_payload)

            node_id = data.get("node", "999")

            message = {
                "meta": {
                    "protocol": "mqttkit1",
                    "network": str(self.protocol_class.network_id),
                    "gateway": str(self.protocol_class.gateway_id),
                    "node": node_id,
                },
                "data": data,
            }

            self.mqtt.publish_json(message)

        elif payload.startswith("value:"):
            json_payload = payload.replace("value:", "")
            data = json.loads(json_payload)

            first = data.items()[0]
            name = first[0]
            value = first[1]

            # print name, value

            message = {
                "meta": {
                    "protocol": "mqttkit1",
                    "network": str(self.protocol_class.network_id),
                    "gateway": str(self.protocol_class.gateway_id),
                    "node": 999,
                },
                "data": data,
            }

            self.mqtt.publish_value(message, name, value)

        # Decode JobeeMonitor line format
        # id=Danvou;lux=13940.88;bmpP=997.03;bmpT=20.32;topT=0;entryT=0;h=70.55;siT=19.38;rainLevel=2.24;RainFall=466;milli=332143870;
        elif payload.startswith("id=") and ";" in payload:
            data = jobee_decode(payload)
            nodeid = data["id"]
            del data["id"]

            # Build an appropriate message from Jobee data
            message = {
                "meta": {
                    "network": str(self.protocol_class.network_id),
                    "gateway": str(self.protocol_class.gateway_id),
                    "node": nodeid,
                },
                "data": data,
            }
            self.mqtt.publish_flexible(message)

        else:
            self.publish_real(payload)

        self.mqtt.mqttc.loop_stop()

    def publish_real(self, payload):

        # decode wire format
        data = self.protocol_class.decode(payload)
        logger.debug("data: {}".format(data))

        if self.protocol_class.VERSION == 1:
            data = self.protocol_class.to_v2(data)

        # publish to MQTT
        self.mqtt.publish_flexible(data, bencode_raw=payload)

    def __del__(self):
        if hasattr(self, "mqtt"):
            logger.info("Disconnecting from MQTT broker")
            self.mqtt.close()


def random_temp():
    return round(random.uniform(7, 26), 2)


def random_hum():
    return round(random.uniform(3, 11), 2)


def random_weight():
    return round(random.uniform(100, 130), 2)


def scale_100(temp):
    return int(temp * 100)


if __name__ == "__main__":
    DataToMQTT(mqtt_broker=sys.argv[1], protocol=1).setup().publish(sys.argv[2])
