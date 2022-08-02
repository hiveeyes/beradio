.. include:: links.rst

.. _beradio-hiveeyes:

###################
BERadio at Hiveeyes
###################


Introduction
============
*BERadio* is used as ether transport at the `Hiveeyes <https://hiveeyes.org/>`__ project.
Some specific information related to that is collected here.


Platform services
=================
Entrypoints to the `Hiveeyes system`_ running on ``swarm.hiveeyes.org`` as of 2016-01-29:

- | Mosquitto
  | mqtt://swarm.hiveeyes.org
- | Grafana
  | https://swarm.hiveeyes.org/grafana/


Submit data
===========
After receiving data from radio link channels, a gateway/concentrator machine
usually forwards it over IP. At the :ref:`Hiveeyes system <hiveeyes-system>`, we use MQTT over TCP/IP.
Get an idea about how this works.

Read BERadio messages from serial interface and forward them to the MQTT broker
on ``swarm.hiveeyes.org`` using the realm ``hiveeyes`` as topic prefix::

    beradio forward --source='serial:///dev/ttyUSB0' --target='mqtt://username:password@swarm.hiveeyes.org/hiveeyes'


.. note::

    The MQTT topic name used for publishing is derived from some parameters contained
    in the data of the message, the topic template used for this is currently programmed
    to ``{realm}/{network}/{gateway}/{node}/{field}``, where ``realm=hiveeyes``.
    The actual values will get separated, mapped and formatted in different
    variants before republishing them to MQTT.


Receive data
============
``bemqtt`` is a basic but convenient MQTT subscriber for setup, testing and debugging.

Subscribe to all messages of the hiveeyes realm::

    bemqtt subscribe --source=mqtt://swarm.hiveeyes.org/hiveeyes

Subscribe to messages of a specific network::

    bemqtt subscribe --source=mqtt://swarm.hiveeyes.org/hiveeyes/696e4192-707f-4e8e-9246-78f6b41a280f

Subscribe to values of a single sensor::

    bemqtt subscribe --source=mqtt://swarm.hiveeyes.org/hiveeyes/696e4192-707f-4e8e-9246-78f6b41a280f/tug22/999/temp1


Architecture
============
We are standing on the shoulders of giants.
Read about the technologies, standards, protocols and subsystems
used for building the whole system at :ref:`hiveeyes-system`.

Read more about the :ref:`hiveeyes-one-architecture` and different
scenarios the components are used in, like :ref:`hiveeyes-one-swarm-setup`
and :ref:`hiveeyes-one-island-setup`.
