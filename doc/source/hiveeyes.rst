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
Entrypoints to the `Hiveeyes platform`_ running on ``swarm.hiveeyes.org`` as of 2016-01-29:

- | Mosquitto
  | mqtt://swarm.hiveeyes.org
- | Grafana
  | https://swarm.hiveeyes.org/grafana/


Submit data
===========
After receiving data from radio link channels, a gateway/concentrator machine
usually forwards it over IP. At :ref:`Hiveeyes <hiveeyes>`, we use MQTT over TCP/IP.
Get an idea about how this works.


Quickstart
----------
Forward BERadio messages to ``swarm.hiveeyes.org``::

    make forward-swarm


Running the forwarder
---------------------
Run ``beradio`` serial-to-mqtt forwarder on a Raspberry Pi acting as a gateway. We will use ``tmux``.
::

    # login and prepare tmux session
    ssh -p 222 he-devs@einsiedlerkrebs.ddns.net
    tmux new -s beradio

    # wo d' musi spuit
    cd ~/hiveeyes/beradio

    # start forwarder
    make forward-swarm


Attach to running instance::

    # login and prepare tmux session
    ssh -p 222 he-devs@einsiedlerkrebs.ddns.net

    # attach to session
    tmux att -t beradio



Subscribe to bus messages
-------------------------

``bemqtt`` is a basic but convenient MQTT subscriber for setup, testing and debugging.

Subscribe to the catch-all MQTT topic of the total ``hiveeyes`` realm::

    bemqtt subscribe --source=mqtt://swarm.hiveeyes.org

Subscribe to messages of a specific network::

    bemqtt subscribe 696e4192-707f-4e8e-9246-78f6b41a280f --source=mqtt://swarm.hiveeyes.org

Subscribe to values of a single sensor::

    bemqtt subscribe 696e4192-707f-4e8e-9246-78f6b41a280f/tug22/999/temp1 --source=mqtt://swarm.hiveeyes.org
