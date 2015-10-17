#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
import serial
from mqtt import MQTTPublisher
from hiveeyes import HiveeyesWireProtocol, HiveeyesPublisher

"""
Read data in Bencode format from command line, decode and publish via MQTT.

Synopsis::

  python publish.py 192.168.59.103 li100ei99ei1ei2218ei2318ei2462ei2250ee

"""

mqtt_broker = sys.argv[1]
payload = sys.argv[2]

def main():

    # setup MQTT publisher client
    channel = MQTTPublisher(mqtt_broker, timeout=0, topic='hiveeyes')
    channel.connect()

    publisher = HiveeyesPublisher(channel=channel)

    # decode wire format
    data = HiveeyesWireProtocol.decode(payload)
    #print 'data:', data

    # publish to MQTT
    publisher.publish(payload, data)

    channel.close()


if __name__ == '__main__':
    main()
