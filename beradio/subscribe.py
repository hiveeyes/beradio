# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <richard@hiveeyes.org>
# (c) 2015-2018 Andreas Motl <andreas@hiveeyes.org>
import logging
import sys

from beradio.mqtt import BERadioMQTTAdapter

"""
Read data from MQTT topic and print on STDOUT.

Synopsis::

  # subscribe to "hiveeyes/#" topic
  python beradio/subscribe.py 192.168.59.103

  # subscribe to "hiveeyes/999/#" topic
  python beradio/subscribe.py 192.168.59.103 999

"""

logger = logging.getLogger(__name__)


class MQTTSubscriber(object):
    def __init__(self, mqtt_broker, mqtt_topic=None):
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic

    def setup(self):
        try:
            logger.info('Connecting to MQTT broker "{}"'.format(self.mqtt_broker))
            self.mqtt = BERadioMQTTAdapter(self.mqtt_broker, topic=self.mqtt_topic)
        except:  # noqa:E722
            logger.error('Failed to connect to MQTT broker "{}"'.format(self.mqtt_broker))
            raise

        return self

    def subscribe(self, topic):
        if topic:
            topic += "/#"
        else:
            topic = "#"
        self.mqtt.subscribe(topic)
        while self.mqtt.mqttc.loop() == 0:
            pass

    def __del__(self):
        if hasattr(self, "mqtt"):
            logger.info("Disconnecting from MQTT broker")
            self.mqtt.close()


if __name__ == "__main__":
    subtopic = ""
    if len(sys.argv) >= 3:
        subtopic = sys.argv[2]
    MQTTSubscriber(mqtt_broker=sys.argv[1]).setup().subscribe(subtopic)
