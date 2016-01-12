==============
BERadio README
==============

*BERadio* is the ether transport protocol for radio link communication at HiveEyes_.

Together with Kotori_, a multi-channel, multi-protocol data acquisition and graphing toolkit for building telemetry
solutions, it runs the platform ``swarm.hiveeyes.org``.

Feel welcome to join us!

.. note::

    For setup information, directly go to the :ref:`setup` documentation, to get an idea about the featureset,
    take a glimpse into the :ref:`handbook`. If you want to modify the source to adapt to your needs,
    you might want to look at :ref:`hacking`.



About
=====

*BERadio* is a specification and provides a reference implementation for Arduino and Python.

- It uses the ``Bencode`` format on the wire to provide space-efficient data encoding.
- ``beradio forward`` processes data messages received over the air and forwards them to MQTT.
- ``libberadio`` will be an appropriate C++ library for Arduino.


Specification
-------------

.. toctree::
    :maxdepth: 2

    beradio


Applications
------------
There are a number of Arduino sensor nodes in the field communicating unidirectionally via radio link to a central
Arduino in a role as a gateway. The gateway Arduino receives message payloads and writes them verbatim to the serial
port connected to a Raspberry Pi, which transforms and forwards the messages to a MQTT bus.

The data now being on the bus, arbitrary systems can consume information by subscribing to specific topics where
measurement events are delivered. The most-wanted requirement, to store the measurements into a solid timeseries database
and to access and display them in a convenient way, is already implemented by the associated `Kotori DAQ`_ project.


Implementation
--------------
``beradio forward`` ingests message payloads from a serial interface, sanitizes and
decodes them from ``Bencode`` format and publishes its data to a MQTT topic.

The topic name is derived from some parameters contained in the data of the message, the topic template used for this
is currently programmed to ``{topic}/{network_id}/{gateway_id}/{node_id}/{name}``, where ``topic=hiveeyes``.
The actual values will get separated and mapped - currently in code - and formatted in various kinds when
republishing them to MQTT.


Architecture
============




Scenario 1  » The "island" setup «
----------------------------------

Run all the infrastructure on your own systems.

- N Arduino sensor nodes
- 1 Arduino gateway node
- 1 Raspberry data acquisition host

::

    Node [AS]    -->    BERadio    -->   Serial [AG] ---> Serial [L] --> MQTT [L] --> Kotori DAQ --> InfluxDB --> Grafana
    |                      |                          |                                                                 |
    |    N sensor nodes    |    1 RFM gateway node    |                    1 data acquisition host                      |
    |                      |                          |                                                                 |
    |                                                 |                                                                 |
    |                  [Arduino]                      |                           [Linux]                               |
    |                                                 |                                                                 |

    Legend:
    [AS]        Arduino sensor node
    [AG]        Arduino gateway node
    [L]         Linux Host
    BERadio     Bencode over Radio


Using this picture, it's easier to point at the place of ``beradio forward``, it helps at the step::

    Serial [L] --> MQTT [L]


Scenario 2  » The "swarm" setup «
---------------------------------

Participate in collaborative data collecting and citizen science projects. Share and compare data with others.

- N Arduino sensor nodes
- 1 Arduino gateway node
- 1 Raspberry gateway host
- 1 Data collector platform

LAN::

    Node [AS]    -->    BERadio    -->    Serial [AG] ---> Serial [L]   -->   MQTT [L]
    |                      |                           |                             |
    |    N sensor nodes    |    1 RFM gateway node     |  1 internet gateway (MQTT)  |
    |                      |                           |                             |
    |                                                  |                             |
    |                  [Arduino]                       |          [Linux]            |
    |                                                  |                             |

WAN::

    MQTT [L] --------------> MQTT [swarm.hiveeyes.org] --> Kotori DAQ --> InfluxDB --> Grafana
    |                    |                                                                   |
    |  internet gateway  |                     1 data acquisition platform                   |
    |                    |                                                                   |


Future
======
- Complete bidirectional communication, to make sensor nodes receive commands over the air, e.g. for maintenance purposes.
  That said, the stack is still lacking the whole chain of::

    MQTT [Linux] --> Serial [Linux] --> Serial [Arduino] --> BERadio --> Node [Arduino]

- Maybe send Bencode encoded ''structures'' over the air, to retain mapping information. This would empower sensor nodes
  at the beginning of the chain to add named sensor points on demand. It will increase payload size, though.

- Improve error handling and overall robustness.
  - decoding ack back to node


Technologies
============
About technologies, standards, protocols and platforms used. Standing on the shoulders of giants.

- Protocols
    - `Bencode encoding <https://en.wikipedia.org/wiki/Bencode>`__, a simple encoding for storing and transmitting loosely structured data.
    - `MQTT <http://mqtt.org/>`__. MQ Telemetry Transport, an extremely lightweight publish/subscribe messaging transport.
    - `WAMP <http://wamp-proto.org/>`__  - The Web Application Messaging Protocol. WAMP is an open standard WebSocket subprotocol that provides Remote Procedure Calls + Publish & Subscribe messaging patterns in one unified protocol.

- Open source components
    - `RFM69 library <https://github.com/LowPowerLab/RFM69>`__, a paramount RFM69 radio link library for RFM69W and RFM69HW on Arduino.
    - `Mosquitto <http://mosquitto.org/>`__, an open-source MQTT v3.1/v3.1.1 Broker.
    - `Kotori DAQ <https://docs.elmyra.de/isar-engineering/kotori-daq/>`__, a multi-channel, multi-protocol data acquisition and graphing toolkit.
        - `Twisted <https://twistedmatrix.com/>`__, an event-driven networking framework.
        - `Autobahn <http://autobahn.ws/>`__, an open-source real-time framework for Web, Mobile & Internet of Things.
    - `InfluxDB <https://influxdb.com/>`__, an open-source distributed time series database.
    - `Grafana <http://grafana.org/>`__, the leading graph and dashboard builder for visualizing time series metrics.

- Commodity platforms
    - `Arduino <https://www.arduino.cc/>`__, an open-source electronics platform based on easy-to-use hardware and software.
    - `Linux <https://www.kernel.org/>`__, the famous free operating system for personal computers based on the Intel x86 architecture having the largest installed base of all general-purpose operating systems.
    - `Python <https://www.python.org/>`__, a programming language that lets you work quickly and integrate systems more effectively.


Credits
=======
- Weef for suggesting the Bencode_ format and Franky for giving support to implement it.
- Chaos Communication Camp 2015 for actually making that happen.
- `A Python script to push serial data to MQTT <http://air.imag.fr/index.php/Mosquitto#Publication_en_Python>`__
  for getting us started on the MQTT_ side based on work from Andy Piper (2011) and Didier Donsez (2014).
    - http://andypiper.co.uk
    - http://lig-membres.imag.fr/donsez/


.. include:: links.rst
