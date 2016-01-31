.. _tasks:

=====
Tasks
=====

Prio 1
------
- [x] properly finish beradio-2 convenience in forwarding and manipulation code
- [x] don't pretend on nodeid=2, neither use it for documentation, use nodeid=999 instead!
- [x] release management
- [x] add software tests
- [x] start with libberadio c++
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
- [o] API docs do not work! https://hiveeyes.org/docs/beradio/api.html


Prio 2
------
- [o] improve docs
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
- [o] care about proper addressing: e.g. take address information completely out of the message, but use identifier from gateway instead!?
- [o] refactor out topic computation from MQTTPublisher.publish_point
- [o] take a look at https://docs.internetofthings.ibmcloud.com/messaging/payload.html

Prio 3
------
- [o] docs: What about other bus systems, like WAMP? See also https://github.com/goeddea/scratchbox/blob/master/yun/serial_to_wamp.js
- [o] make some slides

Prio 4
------

Generalize and split core functionality into separate package "mqttkit". Host on mqttkit.org

mqttkit ideas
=============
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


Collected stuff
---------------
- | random number sender example
  | https://github.com/LowPowerLab/RFM69/blob/master/Examples/RandomNumbers/RandomNumbers.ino
- https://github.com/GreyGnome/EnableInterrupt
- Online Bencode decoder
  - http://jeelabs.net/boards/6/topics/148?r=152#message-152
