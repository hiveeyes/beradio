=====================
serial-to-mqtt README
=====================

Hint: For setup information, directly go to `<doc/setup.rst>`__, to get an idea about the featureset, take a glimpse into `<doc/handbook.rst>`__. If you want to modify the source to adapt to your needs, you might want to look at `<doc/hacking.rst>`__.


About
=====

``serial-to-mqtt`` receives telemetry data over the air and feeds them into the MQTT bus. It ingests payloads from a serial interface, sanitizes
and decodes them from ``Bencode`` format and publishes its data to a MQTT topic. The topic name is derived from some parameters contained in the data of the message, the topic template used for this is currently programmed to ``{topic}/{network_id}/{gateway_id}/{node_id}/{name}``, where ``topic=hiveeyes``. The actual values will get separated and mapped - currently in code - and formatted in different kinds when republishing them to MQTT.

To get an idea how things are translated, let's assume we receive this message over the air, encoded using ``Bencode`` format::

    li999ei99ei1ei2218ei2318ei2462ei2250ee

which will get translated into these distinct MQTT messages::

    hiveeyes/999/1/99/temp1             22.18
    hiveeyes/999/1/99/temp2             23.18
    hiveeyes/999/1/99/temp3             24.62
    hiveeyes/999/1/99/temp4             22.5
    hiveeyes/999/1/99/message-bencode   li999ei99ei1ei2218ei2318ei2462ei2250ee
    hiveeyes/999/1/99/message-json      {"network_id": 999, "node_id": 99, "gateway_id": 1, "temp1": 22.18, "temp2": 23.18, "temp3": 24.62, "temp4": 22.5}

The redundant transfer is justified by satisfying two distinct demands:

- Data should have the discrete value published to a specific topic in order to let generic devices subscribe to the raw sensor value. Example::

    hiveeyes/999/1/99/temp1             22.18

- Data should be sent blockwise in messages in order to make mapping, forwarding and storing more straight-forward. Example::

    hiveeyes/999/1/99/message-json      {"network_id": 999, "node_id": 99, "gateway_id": 1, "temp1": 22.18, "temp2": 23.18, "temp3": 24.62, "temp4": 22.5}

  After minor manipulation, this is stored directly into InfluxDB.


Architecture
============


Intro
-----
There are a number of Arduino sensor nodes in the field communicating unidirectionally via radio link to a central Arduino in a role as a gateway. The gateway Arduino receives message payloads and writes them verbatim to the serial port connected to a Raspberry Pi, which transforms and forwards the data to a MQTT bus. The data now being on the bus, arbitrary systems can consume the information by subscribing to specific topics where data changes are delivered. The most popular use-case, to store the measurements into a modern time-series database, as well as accessing and displaying them in a convenient way, is already implemented by associated projects.


Scenario 1, aka. » The "island" setup «
---------------------------------------

Run all the infrastructure on your own systems.

- N Arduino sensor nodes
- 1 Arduino gateway node
- 1 Raspberry data acquisition host


Sensor nodes::

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


Scenario 2, aka. » The "swarm" setup «
--------------------------------------

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
    |                    |                                                                    |
    |  internet gateway  |                     1 data acquisition platform                    |
    |                    |                                                                    |
    |                                                                                         |
    |                                        [Linux]                                          |
    |                                                                                         |


Future
======
- Complete bidirectional communication, to make sensor nodes receive commands over the air, e.g. for maintenance purposes. That said, the stack is still lacking the whole chain of::

    MQTT [Linux] --> Serial [Linux] --> Serial [Arduino] --> Bencode-over-RFM69 --> Node [Arduino]

- Maybe send Bencode encoded '''structures''' over the air, to retain mapping information. This would empower sensor nodes at the beginning of the chain to add named sensor points on demand. It will increase payload size, though.

- Improve error handling and overall robustness.
