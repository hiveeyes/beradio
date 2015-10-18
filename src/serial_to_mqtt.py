#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
import serial
import bencode
from mqtt import MQTTPublisher
from hiveeyes import HiveeyesWireProtocol, HiveeyesPublisher

"""
Read data in Bencode format from serial port, decode and publish via MQTT.

Based on code from
- Andy Piper http://andypiper.co.uk [2011/09/15]
- Didier Donsez [2014‎/11/22]
  http://air.imag.fr/index.php/Mosquitto#Publication_en_Python

Synopsis::

  python serial_to_mqtt.py /dev/ttyUSB0 localhost
  python serial_to_mqtt.py /dev/ttyACM0 localhost

"""

serial_device = sys.argv[1]
mqtt_broker = sys.argv[2]

mqtt = MQTTPublisher(mqtt_broker, timeout=0, topic='hiveeyes')

publisher = HiveeyesPublisher(channel=mqtt)

# called on exit
# close serial, disconnect MQTT
def cleanup():
    print "Ending and cleaning up"
    ser.close()
    mqtt.close()

try:
    # connect to serial port
    print "Connecting to serial port device", serial_device
    #ser = serial.Serial(serial_device, 9600, timeout=20)
    ser = serial.Serial(serial_device, 115200)

except:
    print "Failed to connect to serial port device", serial_device
    raise SystemExit


if __name__ == '__main__':

    try:
        ser.flushInput()

        # remain connected to broker
        # read data from serial and publish
        while mqtt.mqttc.loop() == 0:

            print '-' * 42

            # read line from serial port
            # li100ei99ei1ei2218ei2318ei2462ei2250ee\0\n
            # li100ei99ei1ei2231ei2325ei2443ei2262ee\0\n
            line = ser.readline()

            # debug: output line to stdout
            print 'line from serial port: "{}"'.format(line)

            # decode from Bencode format
            data = HiveeyesWireProtocol.decode(line)
            #print 'data:', data

            # publish to MQTT
            if data:
                raw_sanitized = HiveeyesWireProtocol.sanitize(line)
                publisher.publish(raw_sanitized, data)

        print 'INFO: Fell out of MQTT main loop'


    # handle list index error (i.e. assume no data received)
    except (IndexError):
        print "No data received within serial timeout period"
        cleanup()

    # handle app closure
    except (KeyboardInterrupt):
        print "Interrupt received"
        cleanup()

    except (RuntimeError):
        print "uh-oh! time to die"
        cleanup()
