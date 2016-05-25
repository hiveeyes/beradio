.. contents:: Sections on this page
   :local:
   :depth: 1

----

.. _tasks:
.. _ideas:

#####
Ideas
#####


****
2016
****


2016-04-25
==========

radino
------
- http://wiki.in-circuit.de/index.php5?title=radino_Modules
- http://busware.de/tiki-index.php
- http://wiki.in-circuit.de/index.php5?title=radino_RF69
- http://shop.busware.de/index.php/cPath/1


2016-04-12
==========
- [o] Add reference to RFM69_ to Intro
- [o] Collected from notes:

    - RFM69 payload size & fragmentation, see RF69_MAX_DATA_LEN
    - emon forschungsprojekt von christoph
    - emon basiert auf RF12? => RFM69!


2016-03-07
==========
- [o] Lua implementation for OpenWrt_ and ESP8266/NodeMCU_

    - https://github.com/nodemcu/nodemcu-firmware#connect-to-mqtt-broker


2016-02-26
==========
Emon goes MQTT!

- https://github.com/emoncms/nodes
- https://github.com/emoncms/emoncms/blob/master/docs/RaspberryPi/MQTT.md
- https://github.com/openenergymonitor/emonhub/blob/emon-pi/src/interfacers/emonhub_interfacer.py


2016-02-20
==========
- [o] Maybe use clint for configuration file and command line arguments
  https://pypi.python.org/pypi/clint/
- [o] update Sphinx theme: https://github.com/kennethreitz/kr-sphinx-themes
- [o] Check out LLVM for AVR
    - https://github.com/avr-llvm/llvm
    - http://lists.llvm.org/pipermail/llvm-dev/2015-September/090038.html
    - http://lists.llvm.org/pipermail/llvm-dev/2015-September/090902.html
    - http://blog.tzikis.com/?p=454
    - https://www.phoronix.com/scan.php?page=news_item&px=LLVM-AVR-Backend-In-Works
    - https://forum.sparkfun.com/viewtopic.php?f=7&t=32665
    - https://stackoverflow.com/questions/19006000/how-to-compile-clang-to-use-as-compiler-for-avr

2016-01-12
==========
- [x] use sawtooth signal instead of random data for pretending
- [x] maybe use a pronounceable label as gateway id
    - https://github.com/greghaskins/gibberish
- [x] use shorter unique id as gateway id
    - http://www.anotherchris.net/csharp/friendly-unique-id-generation-part-1/
    - http://www.anotherchris.net/csharp/friendly-unique-id-generation-part-2/
- [x] send timestamp along, InfluxDB stores "2015-11-14T16:29:42.157025953Z"
- [x] use "-mcall-prologues" for producing smaller binaries 7024
- [o] --interval option for publishers
- [o] Don't decode empty strings: ERROR: Decoding BERadio version 2 data "" failed: not a valid bencoded string
- [x] API docs do not work! https://hiveeyes.org/docs/beradio/api.html
- [o] Generalize and split core functionality into separate package "mqttkit". Host on mqttkit.org

improve documentation
---------------------
    - [o] move some stuff out of README.rst, place into network.rst and also publish @ kotori-daq
    - [o] add docs/rationale about choosing Bencode with reference to JeeLabs
    - [o] aggregate all external http references into links.rst
    - [o] move stuff to Kotori, improve Hiveeyes use-case
    - [o] add graphviz picture via Sphinx extension "sphinx.ext.graphviz"::

        .. graphviz::

            digraph fas_components {
                rankdir=TB;
                ranksep=1;
                node[shape="box", fontname="Verdana"];
                edge[fontname="Verdana"];
                    "FAS" -> "Janitor";
                    "FAS" -> "Unique Object Keys";
                    "FAS" -> "Signed Objects";
                    "Janitor"[shape=record, label="{ Janitor | Authentication }"];
                    "Janitor" -> "Routing";
                    "Janitor" -> "Piggyback Events";
                    "Unique Object Keys"[shape=record, label="{ Unique Object Keys | Entity addressing }"];
                    "Signed Objects"[shape=record, label="{ Signed Objects | { Authorization | Inter-Service-Communication } }"];
            }
    - [o] maybe also try Sphinx extensions "sphinxcontrib.seqdiag, sphinxcontrib.blockdiag or sphinxcontrib.nwdiag",
          see dev/vz/documentation/meta/src/conf.py
    - [o] improve inline docs
    - [o] integrate essentials from "parsing-c-headers.rst" into applications/lst.rst

- [o] finish libberadio c++

    - [o] avr-stl-1.1.2 and Embencode-+1
    - [o] message sending

- [o] properly handle profile => ruleset dispatching
- [o] take a look at https://docs.internetofthings.ibmcloud.com/messaging/payload.html

mqttkit ideas
-------------
- The message broker supports clients connecting with the HTTP protocol using a REST API.
  Clients can publish by sending a POST message to "<AWS IoT Endpoint>/topics/<url_encoded_topic_name>?qos=1"
- use paho instead of mosquitto
- integrate
    - https://pypi.python.org/pypi?%3Aaction=search&term=mqtt&submit=search
    - https://pypi.python.org/pypi/thingpin
    - https://github.com/ibm-messaging/iot-python
    - https://pypi.python.org/pypi/mqtt-randompub
    - http://affolter-engineering.ch/mqtt-randompub/
    - https://pypi.python.org/pypi/mqtt-watchdir
    - https://pypi.python.org/pypi/thingpin
- use "standard" json payload: https://docs.internetofthings.ibmcloud.com/messaging/payload.html
- beacons
    - time
    - weather
- try to run on pypy, jitpy, cython, numba or ... to get tighter timings


****
2015
****


2015-11-02
==========
- [o] make some slides
- | random number sender example
  | https://github.com/LowPowerLab/RFM69/blob/master/Examples/RandomNumbers/RandomNumbers.ino
- https://github.com/GreyGnome/EnableInterrupt
- Online Bencode decoder
  - http://jeelabs.net/boards/6/topics/148?r=152#message-152

2015-10-28
==========
- [x] release management
- [x] add software tests

Goals
-----
- Complete bidirectional communication, to make sensor nodes receive commands over the air, e.g. for maintenance purposes.
  That said, the stack is still lacking the whole chain of::

    MQTT [Linux] --> Serial [Linux] --> Serial [Arduino] --> BERadio --> Node [Arduino]

- Maybe send Bencode encoded ''structures'' over the air, to retain mapping information. This would empower sensor nodes
  at the beginning of the chain to add named sensor points on demand. It will increase payload size, though.

- Improve error handling and overall robustness.
  - decoding ack back to node


2015-10-27
==========
- [x] don't pretend on nodeid=2, neither use it for documentation, use nodeid=999 instead!

2015-10-26
==========
- [x] properly finish beradio-2 convenience in forwarding and manipulation code
- [x] start with libberadio c++

2015-10-25
==========
- [o] care about proper addressing: e.g. take address information completely out of the message, but use identifier from gateway instead!?
- [o] refactor out topic computation from MQTTPublisher.publish_point
- [o] docs: What about other bus systems, like WAMP? See also https://github.com/goeddea/scratchbox/blob/master/yun/serial_to_wamp.js


----


####
Todo
####

List of collected ``.. todo::`` admonitions:

.. todoList::
