##############
BERadio README
##############

.. tip::

    You might want to continue reading at the `official BERadio documentation`_,
    all inline links will be working there.

*****
About
*****
*BERadio* is an encoding specification and implementation for efficient communication in
constrained radio link environments.
It is conceived and used for over-the-air communication within the `Hiveeyes project`_.

Together with Kotori_, a multi-channel, multi-protocol data acquisition and graphing toolkit
for building flexible telemetry solutions, it powers the `Hiveeyes system`_
on the gateway side, which you can enjoy by visiting the `Hiveeyes platform`_.


***********
Environment
***********
There are a number of Arduino sensor nodes in the field communicating unidirectionally
via radio link to a central Arduino acting as a gateway. The gateway Arduino receives
message payloads and writes them verbatim to the serial port connected to a Raspberry Pi,
which transforms and forwards the messages to a MQTT bus.

The data now being on the bus, arbitrary systems can consume information by subscribing
to specific MQTT topics where measurement events are delivered.

The Kotori multichannel DAQ subscribes to topics on the MQTT bus, receives telemetry data
payloads and stores the measurements into a contemporary timeseries database.
After that, Grafana is used to display the measurement information.


*******
Details
*******

Features
========
*BERadio* is a specification and also provides reference implementations for Arduino and Python.

- Some details have been written down in the `BERadio specification`_ document.
- It uses the ``Bencode`` format on the wire to provide space-efficient data encoding.
- ``beradio forward`` processes data messages received over the air and forwards them to MQTT.
- ``libberadio`` will be an appropriate C++ library for Arduino.


The main workhorse
==================
``beradio forward`` ingests message payloads from a serial interface, sanitizes and
decodes them from ``Bencode`` format and republishes the data to a MQTT topic.

The MQTT topic name used for publishing is derived from some parameters contained
in the data of the message, the topic template used for this is currently programmed
to ``{realm}/{network}/{gateway}/{node}/{field}``.
The actual values will get separated, mapped and formatted in different
variants before republishing them to MQTT.


*******************
Project information
*******************

Contributing
============
We are always happy to receive code contributions, ideas, suggestions
and problem reports from the community.
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue ticket.

Thanks in advance for your efforts, we really appreciate any help or feedback.

License
=======
This software is copyright © 2015-2022 The Hiveeyes developers. All rights reserved.

Use of the source code included here is governed by the
`GNU Affero General Public License <GNU-AGPL-3.0_>`_ and the
`European Union Public License <EUPL-1.2_>`_.
The software is and will always be **free and open source software**.


.. _GNU-AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0-standalone.html
.. _EUPL-1.2: https://opensource.org/licenses/EUPL-1.1



.. _official BERadio documentation: https://hiveeyes.org/docs/beradio/
.. _Kotori: https://getkotori.org/
.. _Hiveeyes project: https://hiveeyes.org/
.. _Hiveeyes system: https://hiveeyes.org/docs/system/
.. _Hiveeyes platform: https://swarm.hiveeyes.org/
.. _Bencode: https://en.wikipedia.org/wiki/Bencode
.. _BERadio specification: https://hiveeyes.org/docs/beradio/beradio.html
