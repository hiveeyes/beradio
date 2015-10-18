#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
import serial
import random
from mqtt import MQTTPublisher
from hiveeyes import HiveeyesWireProtocol, HiveeyesPublisher

"""
Read data in Bencode format from command line, decode and publish via MQTT.

Synopsis::

  # send given Bencode payload
  python publish.py 192.168.59.103 li100ei99ei1ei2218ei2318ei2462ei2250ee

  # send random values
  python publish.py 192.168.59.103 random

"""

mqtt_broker = sys.argv[1]
payload = sys.argv[2]

def random_temp():
    return round(random.uniform(7, 26), 2)

def temp_scale(temp):
    return int(temp * 100)

def main():

    global payload

    # setup MQTT publisher client
    channel = MQTTPublisher(mqtt_broker, timeout=0, topic='hiveeyes')

    publisher = HiveeyesPublisher(channel=channel)

    if payload == 'random':
        fields = [
            '999', '99', '1',
            temp_scale(random_temp()), temp_scale(random_temp()), temp_scale(random_temp()), temp_scale(random_temp()),
        ]
        payload = HiveeyesWireProtocol.encode(fields)
        print 'payload:', payload


    # decode wire format
    data = HiveeyesWireProtocol.decode(payload)
    #print 'data:', data

    # publish to MQTT
    publisher.publish(payload, data)

    channel.close()


if __name__ == '__main__':
    main()
