.. image:: https://github.com/hiveeyes/beradio/workflows/Tests/badge.svg
    :target: https://github.com/hiveeyes/beradio/actions?workflow=Tests
    :alt: CI outcome

.. image:: https://codecov.io/gh/hiveeyes/beradio/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/hiveeyes/beradio
    :alt: Test suite code coverage

.. image:: https://pepy.tech/badge/beradio/month
    :target: https://pypi.org/project/beradio/
    :alt: PyPI downloads per month

.. image:: https://img.shields.io/pypi/v/beradio.svg
    :target: https://pypi.org/project/beradio/
    :alt: Package version on PyPI

.. image:: https://img.shields.io/pypi/status/beradio.svg
    :target: https://pypi.org/project/beradio/
    :alt: Project status (alpha, beta, stable)

.. image:: https://img.shields.io/pypi/pyversions/beradio.svg
    :target: https://pypi.org/project/beradio/
    :alt: Support Python versions

.. image:: https://img.shields.io/pypi/l/beradio.svg
    :target: https://github.com/hiveeyes/beradio/blob/main/LICENSE
    :alt: Project license

|

##############
BERadio README
##############

.. tip::

    You might want to continue reading at the official `BERadio documentation`_,
    all inline links will be working there.

*****
About
*****

*BERadio* is an encoding specification and implementation for efficient
communication in constrained radio link environments. It is conceived and used
for over-the-air communication within the `Hiveeyes project`_.

Together with `Kotori`_, a multi-channel, multi-protocol data acquisition and
graphing toolkit for building flexible telemetry solutions, it powers the
`Hiveeyes system`_ on the gateway side, which you can enjoy by visiting the
`Hiveeyes platform`_.


*****
Usage
*****

Handbook
========

The ``beradio`` Python distribution provides convenient commandline-based
decoding tools for working with messages in *Bencode* and *BERadio* formats,
called ``beradio``, ``bdecode``, ``bencode``, and ``bemqtt``.

For more information, have a look at the `BERadio handbook`_.

Synopsis
========

Decoding an example message on the command line.

::

    $ bdecode d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee
    OrderedDict([('#', 999), ('_', 'h1'), ('h', [488, 572]), ('t', [2163, 1925, 1092, 1354]), ('w', 10677)])

::

    $ beradio decode d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee --protocol=2
    {
        "meta": {
            "protocol": "beradio2",
            "network": "b6a6b04c-a929-4a6c-9238-185e9af79eed",
            "gateway": "deh22",
            "node": "999",
            "time": 1659487642526373120,
            "profile": "h1"
        },
        "data": {
            "hum1": 4.88,
            "hum2": 5.72,
            "temp1": 21.63,
            "temp2": 19.25,
            "temp3": 10.92,
            "temp4": 13.54,
            "wght1": 106.77
        }
    }




***********
Environment
***********

There are a number of Arduino sensor nodes in the field communicating unidirectional
via radio link to a central Arduino acting as a gateway. The gateway Arduino receives
message payloads and writes them verbatim to the serial port connected to a Raspberry Pi,
which transforms and forwards the messages to a MQTT bus.

The data now being on the bus, arbitrary systems can consume information by subscribing
to specific MQTT topics where measurement events are delivered.

The Kotori multichannel DAQ subscribes to topics on the MQTT bus, receives telemetry data
payloads and stores the measurements into a contemporary time-series database.
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



.. _Bencode: https://en.wikipedia.org/wiki/Bencode
.. _BERadio documentation: https://hiveeyes.org/docs/beradio/
.. _BERadio handbook: https://hiveeyes.org/docs/beradio/handbook.html
.. _BERadio specification: https://hiveeyes.org/docs/beradio/beradio.html
.. _EUPL-1.2: https://opensource.org/licenses/EUPL-1.1
.. _GNU-AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0-standalone.html
.. _Hiveeyes platform: https://swarm.hiveeyes.org/
.. _Hiveeyes project: https://hiveeyes.org/
.. _Hiveeyes system: https://hiveeyes.org/docs/system/
.. _Kotori: https://getkotori.org/
