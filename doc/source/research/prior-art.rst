.. include:: ../links.rst

#########
Prior art
#########

.. contents::
   :local:
   :depth: 2

----

************
Introduction
************

This is all about the air protocol, i.e. state-of-the-art low-range RF communication protocols,
message encapsulation and sending interfaces. We focus on implementations based on the RFM69_
library for Arduino by Felix Rusu but looking for LoRa support.

The document investigates the way how values are actually transmitted over the air and how they are
encoded, especially when it comes to transmitting multiple values at once leading directly
to the question of how much sender and receiver are coupled.


*********************
Serialization formats
*********************

As a general overview, see https://en.wikipedia.org/wiki/Comparison_of_data_serialization_formats

We will define multiple families of encoding/serialization schemes by enumerating some examples.


Family 1: Binary
================
Binary format, usually no message encapsulation, bare struct.

It is very common to define structs and just send them over the air in their respective
binary representation.

This kind of implementation gains a maximum of efficiency::

    >>> import struct
    >>> payload = struct.pack('!ff', 42.42, 99.99)
    >>> payload
    'B)\xae\x14B\xc7\xfa\xe1'
    >>> len(payload)
    8

The drawback is that sender and receiver are tightly coupled by implementing the same
payload struct declaration in order to talk to each other.


Family 2: 8-bit clean
=====================
ASCII format, arbitrary message encapsulation.

To gain more flexibility, 8-bit clean transport protocols are used.
On the pro side, arbitrary convenient and advanced line-based protocols can be designed on top of them.
They are also easy to debug, especially when staring at payloads while receiving or forwarding messages through a serial interface.

TODO: Break out into different section. The drawback here is usually payload size,
since the maximum packet payload size defined in `RFM69.h#L35`_ is 61 bytes::

    // to take advantage of the built in AES/CRC we want to limit the frame size
    // to the internal FIFO size (66 bytes - 3 bytes overhead - 2 bytes crc)
    #define RF69_MAX_DATA_LEN       61

http://www.airspayce.com/mikem/arduino/RadioHead/RH__RF69_8h_source.html::

    // Max number of octets the RH_RF69 Rx and Tx FIFOs can hold
    #define RH_RF69_FIFO_SIZE 66

    // Maximum encryptable payload length the RF69 can support
    #define RH_RF69_MAX_ENCRYPTABLE_PAYLOAD_LEN 64

http://www.airspayce.com/mikem/arduino/RadioHead/RH__RF95_8h_source.html::

    // Max number of octets the LORA Rx/Tx FIFO can hold
    #define RH_RF95_FIFO_SIZE 255


Current implementations
-----------------------
As far as we can see, there is no standardized way of how to actually talk radio across
different open sensor network implementations found in the wild / on github.


How JeeLink does it
~~~~~~~~~~~~~~~~~~~
Type: Binary struct

- http://jeelabs.org/2010/12/07/binary-packet-decoding/
- http://jeelabs.org/2010/07/12/serial-communications-vs-packets/


RFduino
~~~~~~~

... has a nice interface, see `Temperature.ino <https://github.com/RFduino/RFduino/blob/master/libraries/RFduinoBLE/examples/Temperature/Temperature.ino>`_::

    #include <RFduinoBLE.h>

    void setup() {
        // this is the data we want to appear in the advertisement
        // (the deviceName length plus the advertisement length must be <= 18 bytes)
        RFduinoBLE.advertisementData = "temp";

        // start the BLE stack
        RFduinoBLE.begin();
    }

    void loop() {
        // sample once per second
        RFduino_ULPDelay( SECONDS(1) );

        // get a cpu temperature sample
        // degrees c (-198.00 to +260.00)
        // degrees f (-128.00 to +127.00)
        float temp = RFduino_temperature(CELSIUS);

        // send the sample to the iPhone
        RFduinoBLE.sendFloat(temp);
    }

.. seealso::

    `RFduinoBLE.cpp#L94 <https://github.com/RFduino/RFduino/blob/master/libraries/RFduinoBLE/RFduinoBLE.cpp#L94>`_


This is how some RFM69_ examples do it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Type: Binary struct

- `Struct_send.ino#L20 <https://github.com/LowPowerLab/RFM69/blob/master/Examples/Struct_send/Struct_send.ino#L20>`_
- `Struct_receive.ino#L17 <https://github.com/LowPowerLab/RFM69/blob/master/Examples/Struct_receive/Struct_receive.ino#L17>`_

::

    # declare struct
    typedef struct {
        int           nodeId; //store this nodeId
        unsigned long uptime; //uptime in ms
        float         temp;   //temperature maybe?
    } Payload;
    Payload theData;

    # fill struct
    theData.nodeId = NODEID;
    theData.uptime = millis();
    theData.temp = 91.23; //it's hot!

    # transmit struct
    radio.sendWithRetry(GATEWAYID, (const void*)(&theData), sizeof(theData))

    # receive struct
    if (radio.receiveDone()) {
        theData = *(Payload*)radio.DATA;
        Serial.print(theData.nodeId);
        Serial.print(theData.uptime);
        Serial.print(theData.temp);
    }



Here's how an emon sensor node does it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Type: Binary struct

`emonTH_LPL.ino#L27 <https://github.com/openenergymonitor/emonLPL/blob/master/emonTH_LPL/emonTH_LPL.ino#L27>`_::

    // RFM12B RF payload datastructure
    typedef struct {
        int temp;
        int temp_external;
        int humidity;
        int battery;
    } Payload;
    Payload emonth;


`emonTxV3_LPL.ino#L28 <https://github.com/openenergymonitor/emonLPL/blob/master/emonTxV3_LPL/emonTxV3_LPL.ino#L28>`_::

    typedef struct { int power1, power2, power3, power4, vrms; } PayloadTX;
    PayloadTX emontx;


`emonTxV3_4_3Phase_Voltage_LPL.ino#L239 <https://github.com/openenergymonitor/emonLPL/blob/master/emonTxV3_4_3Phase_Voltage_LPL/emonTxV3_4_3Phase_Voltage_LPL.ino#L239>`_::

    // neat way of packaging data for RF comms
    // Include all the variables that are desired,
    // ensure the same struct is used to receive.
    // The maximum size is 60 Bytes
    typedef struct { int power1, power2, power3, va1, va2, va3, Vrms, pnum; } PayloadTX;

    // create an instance
    PayloadTX emontx;


UniMote of CuPID Controls
~~~~~~~~~~~~~~~~~~~~~~~~~
Type: 8-bit clean

CuPID Controls: Networked, flexible control and monitoring for any application.

Colin Reese of `Interface Innovations`_ designed an overlay protocol
over an 8-bit clean data channel for the `CuPID Controls`_ system.
Over that protocol, he is able to completely augment and control
the program running on the target by using user-programmable variables.

The wire message format is very simple::

    ~command;arg1;arg2;arg3

The list of features is really impressive:

- Create an ATMega sketch that allows read/write of all available Moteino IO in all allowable formats by change of variable values, i.e. no code change required
- Allow OneWire read operations on all digital IO  (only for DS18B20s here)
- Configure IO for read and report (broadcast) on remotely adjustable schedule
- Configure channel control, with configurable setpoint and process values and positive and negative feedback
- Set all key program parameters remotely (via radio) and locally (on serial)
- Adjustable, metadata-containing, report format for IO, channels, and system parameters
- Save system configuration to EEPROM and restore upon resume after loss of power

.. seealso::

    - http://www.cupidcontrols.com/2014/08/adventures-in-moteino-remote-temperature-monitor/
    - http://www.cupidcontrols.com/2014/09/adventures-in-moteino-modular-communication-for-cupid-remote/
    - http://www.cupidcontrols.com/2015/03/unimote-v2-read-all-the-rf-things/


The target can be introspected - a picture says a thousand words::

    ~listparams
    Command character received
    NODEID:0,
    GATEWAYID:0,
    NETWORKID:0,
    LOOPPERIOD:2000,
    SLEEPMODE:0,
    iomode:[0,0,0,0,0,3,0,3,0,0,0,0,0],
    ioenabled:[0,0,0,0,0,0,0,0,0,0,0,0,0],
    ioreadfreq:[10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000],
    ioreportenabled:[0,0,0,0,0,0,0,0,0,0,0,0,0],
    ioreportfreq:[0,0,0,0,0,0,0,0,0,0,0,0,0],
    chanenabled:[0,0,0,0,0,0,0,0],
    chanmode:[0,0,0,0,0,0,0,0],
    chanposfdbk:[0,0,0,0,0,0,0,0],
    channegfdbk:[-1,0,0,0,0,0,0,0],
    chandeadband:[0,0,0,0,0,0,0,0],
    chanpvindex:[5,0,0,0,0,0,0,0],
    chansv:[15.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00]


The workhorse command is::

    ~modparam;paramname;index;value


As we are currently interested in sending multiple measurement values (not control commands), here is the place we've found:

`uni_mote_2p75.ino#L1736 <https://github.com/iinnovations/iicontrollibs/blob/master/mote/unimote/uni_mote_2p75/uni_mote_2p75.ino#L1736>`_::

    void sendIOMessage(byte ionum, byte mode, float value) {
        // Initialize send string

        int sendlength = 61;  // default
        if (mode == 0 || mode == 1 ) { // for integer values
            sendlength = 30;
            sprintf(buff, "ionum:%02d,iomode:%02d,ioval:%04d", ionum, mode, value);
            sendWithSerialNotify(GATEWAYID, buff, sendlength, ~serialrfecho);
        }
        else if (mode == 2) { // for float values
            int wholePart = value;
            long fractPart = (value - wholePart) * 10000;
            sendlength = 34;
            sprintf(buff, "ionum:%02d,iomode:%02d,ioval:%03d.%04d", ionum, mode, wholePart, fractPart);
            sendWithSerialNotify(GATEWAYID, buff, sendlength, serialrfecho);
        }
    }

`serialhandler.py#L276 <https://github.com/iinnovations/iicontrollibs/blob/master/mote/serialhandler.py#L276>`_ ff.::

    # [...]
    # Command responses, including value requests
    if 'cmd' in datadict:
        # [...]
        for key in datadict:
            thetime = pilib.gettimestring()
            if key in ['iov', 'iov2', 'iov3', 'pv', 'pv2', 'sv', 'sv2', 'iomd', 'ioen', 'iordf', 'iorpf', 'chen', 'chmd', 'chnf', 'chpf', 'chdb', 'chsv', 'chsv2', 'chpv', 'chpv2']:

    # This is for values that are reported by the node
    elif 'ioval' in datadict:

    elif 'owdev' in datadict:

    elif 'chan' in datadict:

    elif 'scalevalue' in datadict:

    # [...]


Family 3: 8-bit clean, container
================================

Bencode
-------
Jean-Claude Wippler already experimented with Bencode_ and implemented the fine EmBencode_ library for Arduino:
- http://jeelabs.org/2012/06/22/structured-data/
- http://jeelabs.org/?s=bencode

- https://github.com/jcw/jeelib/search?utf8=%E2%9C%93&q=EmBencode
- `rf12cmd.ino <https://github.com/jcw/jeelib/blob/master/examples/RF12/rf12cmd/rf12cmd.ino>`_

It's also mentioned at `Serialization for data exchange between micro processor and the web <http://jeelabs.net/boards/6/topics/2790>`_.

Outlook:

    | You have chosen a very nice and simple defacto data encoding protocol. I hope though that you will be
    | using the extended bencode versions that also allow bool and float to be part of the data… I’m using
    | them a lot for temperatue and humidity for instance!
    |
    | -- http://jeelabs.org/2012/06/22/structured-data/#comment-5591


Discussions
===========

- | You're Using JSON, Why not MessagePack?
  | https://news.ycombinator.com/item?id=2571729


************
API proposal
************

How about?
::

    #include <beradio.h>

    int NODE_ID = 1;
    char * PROFILE_ID = "h1";

    void setup() {
        app_initialize(...);
    }

    void loop() {
        BERadioMessage message(NODE_ID, PROFILE_ID);
        message.temperature(4, 21.63, 19.25, 10.92, 13.54);
        message.voltage(4, 21.63, 19.25, 10.92, 13.54);
        message.send();
        delay(1000);
    }



***********
Inspiration
***********

Projects
========

Jee Labs
--------
- http://jeelabs.org/
- http://jeelabs.org/about/
- https://github.com/jcw/jeelib
- http://jeelabs.net/pub/docs/jeelib/
- http://jeelabs.net/projects/jeelib/wiki
- https://github.com/jcw/housemon
- https://github.com/jcw/metakit
- https://github.com/jeelabs/embello
- https://github.com/jeelabs/jet
- https://github.com/jcw/embencode
- http://jeelabs.net/issues/526


computourist
------------
A RFM69 based sensors and MQTT gateway
- https://github.com/computourist/RFM69-MQTT-client

Sensor node
~~~~~~~~~~~
- https://github.com/computourist/RFM69-MQTT-client/tree/master/DHT%20end%20node
- https://github.com/computourist/RFM69-MQTT-client/tree/master/DIG%20end%20node
- https://github.com/computourist/RFM69-MQTT-client/tree/master/Openhab%20Example

Gateway
~~~~~~~
- https://github.com/computourist/RFM69-MQTT-client/blob/master/Gateway_2.4

Communication
~~~~~~~~~~~~~
- https://github.com/computourist/RFM69-MQTT-client/blob/master/DHT%20end%20node/RFM_DHT_node_22.ino#L118
- https://github.com/computourist/RFM69-MQTT-client/blob/master/Gateway_2.4/RFM_MQTT_GW_24.ino#L21

Outlook
~~~~~~~
- | using serial instead of Ethernet #2
  | https://github.com/computourist/RFM69-MQTT-client/issues/2


ULPNode
-------
- http://hallard.me/ulpnode-rf-protocol/
- https://hallard.me/ulpnode-projet-update/
- https://hallard.me/fixed-usb-dev-uteleinfo/


Serialization
=============

Bencode
-------

Basics
~~~~~~
- https://en.wikipedia.org/wiki/Bencode
- https://github.com/jcw/embencode
- http://jeelabs.org/2012/09/30/sending-bencode-data/
- http://jeelabs.org/2012/10/01/collecting-bencode-data/
- http://jeelabs.org/2012/10/03/decoding-bencode-data/
- http://jeelabs.net/pub/docs/embencode/
- http://jeelabs.org/?s=bencode
- https://github.com/jcw/jeelib/blob/master/examples/RF12/rf12cmd/rf12cmd.ino

More Bencode
~~~~~~~~~~~~
- https://github.com/japeq/bencode-tools
- http://zakalwe.fi/~shd/foss/bencode-tools/
- https://github.com/benjreinhart/bencode-js
- https://github.com/heikkiorsila/bencode-tools
- https://github.com/rchouinard/bencode
- http://effbot.org/zone/bencode.htm
- http://jeelabs.net/boards/6/topics/148
- http://marquisdegeek.com/code_bencode.php
- http://marquisdegeek.com/pub/html5/bencode/
- https://bencode.codeplex.com/



********
Research
********

Technology
==========

RFM generations
---------------
- Hope RF RFM12B
- | Hope RF RFM69
  | http://lowpowerlab.com/blog/2013/06/20/rfm69-library/
  | https://github.com/LowPowerLab/RFM69
  | http://www.airspayce.com/mikem/arduino/RadioHead/classRH__RF69.html
- Semtech LoRa RFM92-RFM98
    - http://lowpowerlab.com/moteino/#lora
    - http://www.instructables.com/id/Introducing-LoRa-/?ALLSTEPS
    - | http://www.airspayce.com/mikem/arduino/RadioHead/classRH__RF95.html
      | - Range over flat ground through heavy trees and vegetation approx 2km.
      | - At 20dBm (100mW) otherwise identical conditions approx 3km.
      | - At 20dBm, along salt water flat sandy beach, 3.2km.


Node hardware
=============
- http://jeelabs.net/projects/hardware/wiki/JeeNode
- http://jeelabs.net/projects/hardware/wiki/JeeNode_Micro
- http://jeelabs.net/projects/hardware/wiki/JeeLink
- http://www.rfduino.com/
    - https://plus.google.com/+DonColeman/posts/d35qg6BEEwv

Bus systems
===========
- JeeBus
    - http://jeelabs.net/projects/housemon/wiki/jeebus
    - https://github.com/jcw/jeebus


The gateways
============

Other serial-to-X forwarders
----------------------------
- https://github.com/crossbario/autobahn-python/blob/master/examples/twisted/wamp/app/serial2ws/serial2ws.py
- https://github.com/goeddea/scratchbox/blob/master/yun/serial_to_wamp.js

MySensors
---------
- https://github.com/mysensors/Arduino/blob/development/libraries/MySensors/examples/GatewayESP8266MQTTClient/GatewayESP8266MQTTClient.ino

Jet
---
A dataflow framework and server for multi-node embedded systems
- https://github.com/jeelabs/jet

LoRa
----
- https://github.com/Lora-net/packet_forwarder

TheThingsNetwork
----------------
- https://github.com/TheThingsNetwork/lora_gateway
    - | Add Mosquitto to server environment
      | https://github.com/TheThingsNetwork/server-devenv/issues/4
- https://github.com/TheThingsNetwork/croft
    - | Post message to MQTT broker
      | https://github.com/TheThingsNetwork/croft/issues/6



C++ interfaces
==============
- c++ interface of http://cnmat.berkeley.edu/library/oscuino/omessage
- https://github.com/mgk/thingamon
- https://github.com/mgk/thingpin
- rfm12-mqtt-gateway
    - https://pypi.python.org/pypi/rfm12-mqtt-gateway/
    - https://pypi.python.org/pypi/rfm12-mqtt-gateway
    - https://github.com/ricklupton/rfm12-mqtt-gateway/blob/master/test/test_node_definition.py



Projects
========

CuPID
-----
- http://www.cupidcontrols.com/2014/02/cupid-touchscreen-touch-my-pi/
- http://www.cupidcontrols.com/2014/04/raspberry-pi-cupid-webio-javascriptjquery-apache-python/
- http://www.cupidcontrols.com/2015/03/rf-mote-web-ui-program-all-the-rf-things/
- https://www.interfaceinnovations.org/ccsoftware.html
- https://www.interfaceinnovations.org/cchardware.html
- https://www.interfaceinnovations.org/cclibsinstall.html
- https://github.com/iinnovations/iicontrollibs/tree/master/cupid
- https://github.com/iinnovations/iicontrollibs/blob/master/misc/hamachidaemon.py

UniMote
-------
Command-/channel based overlay protocol over RF

- https://github.com/iinnovations/iicontrollibs/blob/master/mote/unimote/uni_mote_2p75/uni_mote_2p75.ino#L1736
- https://github.com/iinnovations/iicontrollibs/blob/master/mote/unimote/uni_mote_2p75/uni_mote_2p75.ino#L274
- https://github.com/iinnovations/iicontrollibs/blob/master/mote/gateway/unimote_gateway_1p1/unimote_gateway_1p1.ino
- https://github.com/iinnovations/iicontrollibs/blob/master/mote/remote/uni_mote_2p7/uni_mote_2p7.ino
- https://github.com/iinnovations/iicontrollibs/blob/master/mote/rfcoms.py

SNAP
----
SNAP - an embedded network application platform

- http://synapse-wireless.com/
- | Synapse‘s SNAP Network Operating System
  | http://www.synapse-wireless.com/upl/downloads/industry-solutions/reference/white-paper-synapse-snap-network-operating-system-96f6130b.pdf
- http://www.synapse-wireless.com/iot-products/lighting-controls/snap-the-application-and-network-platform-for-the-internet-of-things-iot/
- http://info.synapse-wireless.com/snap-network-and-application-platform
- http://www.synapse-wireless.com/iot-products/core-iot/software/portal/
- http://www.synapse-wireless.com/upl/downloads/industry-solutions/reference/product-brief-synapse-portal-813f9bd2.pdf
- http://www.synapse-wireless.com/upl/downloads/industry-solutions/reference/reference-manual-synapse-portal-5bfe1af4.pdf
- http://www.synapse-wireless.com/iot-products/core-iot/rf-modules/
- https://www.sparkfun.com/products/11279
- http://www.synapse-wireless.com/about-us/company-history/
- https://www.sparkfun.com/tutorials/367
- http://www.arrownac.com/solutions-applications/machine-to-machine/protocols/snap.php
- https://www.digikey.com/suppliers/us/synapse-wireless.page?&lang=en


The Things Network
------------------
- https://www.kickstarter.com/projects/419277966/the-things-network
- http://www.heise.de/newsticker/meldung/The-Things-Network-Gateway-fuer-200-Euro-funkt-10-Kilometer-weit-2852069.html


More
----
- http://opensoundcontrol.org/spec-1_0
- http://cnmat.berkeley.edu/oscuino
- https://code.google.com/p/arduinode/
- http://harteware.blogspot.de/2011/10/presenting-arduinode-wireless-sensor.html
- http://playground.arduino.cc/Code/Messenger
- http://playground.arduino.cc/Code/CmdMessenger
- http://www.megunolink.com/documentation/plotting/plotting-message-reference/
- https://github.com/dreamcat4/CmdMessenger2
- http://playground.arduino.cc/Code/SimpleMessageSystem


SBMP
----
Simple Binary Messaging Protocol - USART protocol for microcontrollers
- https://github.com/MightyPork/sbmp
- https://github.com/MightyPork/sbmp/tree/master/spec
- https://github.com/MightyPork/sbmp/blob/master/spec/DATAGRAMS.md
- https://github.com/MightyPork/sbmp/blob/master/spec/FRAMING_LAYER.md
-