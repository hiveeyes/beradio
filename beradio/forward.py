#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import serial
from mqtt import BERadioMQTTPublisher
from beradio.protocol import get_protocol_class

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

class SerialToMQTT(object):

    def __init__(self, serial_device, mqtt_broker, mqtt_topic='hiveeyes', protocol=2):
        self.serial_device = serial_device
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic
        self.protocol_class = get_protocol_class(protocol)

    def setup(self):

        try:
            # connect to serial port
            print 'INFO:  Connecting to serial port device "{}"'.format(self.serial_device)
            #self.serial = serial.Serial(serial_device, 9600, timeout=20)
            self.serial = serial.Serial(self.serial_device, 115200)
        except:
            print 'ERROR: Failed to connect to serial port device "{}"'.format(self.serial_device)
            raise SystemExit

        try:
            print 'INFO:  Connecting to MQTT broker "{}"'.format(self.mqtt_broker)
            self.mqtt = BERadioMQTTPublisher(self.mqtt_broker, timeout=0, topic=self.mqtt_topic)
        except:
            print 'ERROR: Failed to connect to MQTT broker "{}"'.format(self.mqtt_broker)
            raise SystemExit

        return self

    def forward(self):

        try:
            self.serial.flushInput()

            # remain connected to broker
            # read data from serial and publish
            while self.mqtt.mqttc.loop() == 0:

                print '-' * 42

                # read line from serial port
                # li999ei99ei1ei2218ei2318ei2462ei2250ee\0\n
                # li999ei99ei1ei2231ei2325ei2443ei2262ee\0\n
                line = self.serial.readline()

                # debug: output line to stdout
                print 'line from serial port: "{}"'.format(line)

                # decode from Bencode format
                data = self.protocol_class.decode(line)
                #print 'data:', data

                # publish to MQTT
                if data:
                    raw_sanitized = self.protocol_class.sanitize(line)
                    self.mqtt.publish_flexible(data, bencode_raw=raw_sanitized)

            print 'INFO: Fell out of MQTT main loop'


        # handle list index error (i.e. assume no data received)
        except (IndexError):
            print "No data received within serial timeout period"
            self.cleanup()

        # handle app closure
        except (KeyboardInterrupt):
            print "Interrupt received"
            self.cleanup()

        except (RuntimeError):
            print "uh-oh! time to die"
            self.cleanup()


    # called on exit
    # close serial, disconnect MQTT
    def cleanup(self):
        print "Ending and cleaning up"
        self.serial.close()
        self.mqtt.close()


if __name__ == '__main__':
    SerialToMQTT(serial_device=sys.argv[1], mqtt_broker=sys.argv[2]).setup().forward()
