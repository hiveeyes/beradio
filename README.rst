=====================
serial-to-mqtt README
=====================

> ``serial-to-mqtt`` plays a little role at `<https://hiveeyes.org/>`__.

Hint: For setup information, directly go to `<doc/setup.rst>`__, to get an idea about the featureset, take a glimpse into `<doc/handbook.rst>`__. If you want to modify the source to adapt to your needs, you might want to look at `<doc/hacking.rst>`__.


About
=====

``serial-to-mqtt`` processes telemetry data received over the air and feeds it into MQTT. It ingests message payloads from a serial interface, sanitizes and decodes them from ``Bencode`` format and publishes its data to a MQTT topic. The topic name is derived from some parameters contained in the data of the message, the topic template used for this is currently programmed to ``{topic}/{network_id}/{gateway_id}/{node_id}/{name}``, where ``topic=hiveeyes``. The actual values will get separated and mapped - currently in code - and formatted in different kinds when republishing them to MQTT.

To get an idea how things are translated, let's assume we receive this message over the air, encoded using ``Bencode`` format::

    li999ei99ei1ei2218ei2318ei2462ei2250ee

which will get translated into these distinct MQTT messages::

    hiveeyes/999/1/99/temp1             22.18
    hiveeyes/999/1/99/temp2             23.18
    hiveeyes/999/1/99/temp3             24.62
    hiveeyes/999/1/99/temp4             22.5
    hiveeyes/999/1/99/message-bencode   li999ei99ei1ei2218ei2318ei2462ei2250ee
    hiveeyes/999/1/99/message-json      {"network_id": 999, "node_id": 99, "gateway_id": 1, "temp1": 22.18, "temp2": 23.18, "temp3": 24.62, "temp4": 22.5}

The redundant transfer is justified by satisfying two contradicting requirements:

- Data should have the discrete value published to a specific topic in order to let generic devices subscribe to the raw sensor value. Example::

    hiveeyes/999/1/99/temp1             22.18

- Data should be sent blockwise in messages in order to make mapping, forwarding and storing more straight-forward. Example::

    hiveeyes/999/1/99/message-json      {"network_id": 999, "node_id": 99, "gateway_id": 1, "temp1": 22.18, "temp2": 23.18, "temp3": 24.62, "temp4": 22.5}

  After minor manipulation, this is stored directly into InfluxDB.


Architecture
============


Intro
-----
There are a number of Arduino sensor nodes in the field communicating unidirectionally via radio link to a central Arduino in a role as a gateway. The gateway Arduino receives message payloads and writes them verbatim to the serial port connected to a Raspberry Pi, which transforms and forwards the data to a MQTT bus. The data now being on the bus, arbitrary systems can consume the information by subscribing to specific topics where data changes are delivered. The most popular use-case, storing as well as accessing and displaying the measurements in a convenient way, is already implemented by associated ''Hiveeyes'' projects.


Scenario 1  » The "island" setup «
----------------------------------

Run all the infrastructure on your own systems.

- N Arduino sensor nodes
- 1 Arduino gateway node
- 1 Raspberry data acquisition host

::

    Node [AS] --> Bencode-over-Radio --> Serial [AG] ---> Serial [L] --> MQTT [L] --> Kotori DAQ --> InfluxDB --> Grafana
    |                      |                          |                                                                 |
    |    N sensor nodes    |    1 RFM gateway node    |                    1 data acquisition host                      |
    |                      |                          |                                                                 |
    |                                                 |                                                                 |
    |                  [Arduino]                      |                           [Linux]                               |
    |                                                 |                                                                 |

    Legend:
    [AS] Arduino sensor node
    [AG] Arduino gateway node
    [L]  Linux Host


Using this picture, it's easier to point at the place of ``serial-to-mqtt``, it helps at the step::

    Serial [L] --> MQTT [L]


Scenario 2  » The "swarm" setup «
---------------------------------

Participate in collaborative data collecting and citizen science projects. Share and compare data with others.

- N Arduino sensor nodes
- 1 Arduino gateway node
- 1 Raspberry gateway host
- 1 Data collector platform

LAN::

    Node [AS] --> Bencode-over-Radio --> Serial [AG] -----> Serial [L] -----> MQTT [L]
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
- Complete bidirectional communication, to make sensor nodes receive commands over the air, e.g. for maintenance purposes. That said, the stack is still lacking the whole chain of::

    MQTT [Linux] --> Serial [Linux] --> Serial [Arduino] --> Bencode-over-Radio --> Node [Arduino]

- Maybe send Bencode encoded ''structures'' over the air, to retain mapping information. This would empower sensor nodes at the beginning of the chain to add named sensor points on demand. It will increase payload size, though.

- Improve error handling and overall robustness.


Technologies
============
About technologies, standards, protocols and platforms used. Standing on the shoulders of giants.

- Protocols
    - `Bencode encoding <https://en.wikipedia.org/wiki/Bencode>`__, a simple encoding for storing and transmitting loosely structured data.
    - `MQTT <http://mqtt.org/>`__. MQ Telemetry Transport, an extremely lightweight publish/subscribe messaging transport.
    - `WAMP <http://wamp-proto.org/>`__  - The Web Application Messaging Protocol. WAMP is an open standard WebSocket subprotocol that provides two application messaging patterns in one unified protocol: Remote Procedure Calls + Publish & Subscribe.

- Components
    - `RFM69 library <https://github.com/LowPowerLab/RFM69>`__, a paramount RFM69 radio link library for RFM69W and RFM69HW.
    - `Mosquitto <http://mosquitto.org/>`__, an open-source MQTT v3.1/v3.1.1 Broker.
    - `Twisted <https://twistedmatrix.com/>`__, an event-driven networking framework.
    - `Autobahn <http://autobahn.ws/>`__, an open-source real-time framework for Web, Mobile & Internet of Things.
    - `InfluxDB <https://influxdb.com/>`__, an open-source distributed time series database.
    - `Grafana <http://grafana.org/>`__, the leading graph and dashboard builder for visualizing time series metrics.

- Platforms
    - Arduino
    - Linux
    - `Python <https://www.python.org/>`__, a programming language that lets you work quickly and integrate systems more effectively.
