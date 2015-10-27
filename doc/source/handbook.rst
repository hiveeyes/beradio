.. _handbook:

========
Handbook
========

.. toctree::
    :maxdepth: 2


Running ``beradio``
===================

Read the source, luke. A good starting point is the ``Makefile``,
then you might want to follow up looking into ``beradio/commands.py``,
``beradio/publish.py`` and ``beradio/forward.py``.

Synopsis::

    # read from serial interface, publish data to the
    # central data collector on ``swarm.hiveeyes.org`` using MQTT
    make forward-swarm

    # read from serial interface, publish data
    # to a MQTT broker running on localhost
    make forward

    # publish fixed Bencode payload to MQTT broker running on localhost, with network=test
    make pretend-local

    # publish random data to ``swarm.hiveeyes.org``, with network=test
    make pretend-swarm-random


Network and gateway identifiers
-------------------------------
On the first time needed, ``beradio`` generates a ``network_id`` and ``gateway_id``,
which get stored persistently.

Display the contents::

    beradio info
    --------------------------------------------------
                      beradio 0.4.0
    --------------------------------------------------
    config file: /Users/amo/Library/Application Support/beradio/config.json
    network_id:  696e4192-707f-4e8e-9246-78f6b41a280f
    gateway_id:  3756780977880301569


On lab gateway using ``tmux``
-----------------------------
Run ``beradio`` forwarder on Raspberry Pi inside ``tmux``::

    # login and prepare tmux session
    ssh -p 222 he-devs@einsiedlerkrebs.ddns.net
    tmux new -s beradio

    # wo d' musi spuit
    cd ~/hiveeyes/beradio

    # start forwarder
    make forward-swarm

    # quick mode does not work, this would close the tmux session when hitting CTRL+C
    #tmux new -s beradio 'bash -c "cd /home/he-devs/hiveeyes/beradio; make forward-swarm; exec bash"'

Attach to running instance::

    # login and prepare tmux session
    ssh -p 222 he-devs@einsiedlerkrebs.ddns.net

    # attach to session
    tmux att -t beradio



.. _handbook-tools:

Tools
=====

Decoding Bencode payloads
-------------------------

This just decodes from Bencode format::

    $ bdecode li999ei99ei1ei2218ei2318ei2462ei2250ee
    [999, 99, 1, 2218, 2318, 2462, 2250]

    $ bdecode d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee
    {'w': 10677, 'h': [488, 572], '#': 999, 't': [2163, 1925, 1092, 1354], '_': 'h1'}


Decoding BERadio messages
-------------------------

Let's throw protocol stuff into the mix. Decode better.

Protocol version 1::

    $ beradio decode li999ei99ei1ei2218ei2318ei2462ei2250ee --protocol=1
    message v1: [999, 99, 1, 2218, 2318, 2462, 2250]
    {
        "network_id": 999,
        "node_id": 99,
        "gateway_id": 1,
        "temp1": 22.18,
        "temp2": 23.18,
        "temp3": 24.62,
        "temp4": 22.5
    }

Protocol version 2::

    $ beradio decode d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee --protocol=2
    message v2: {'w': 10677, 'h': [488, 572], '#': 2, 't': [2163, 1925, 1092, 1354], '_': 'h1'}
    {
        "meta": {
            "node": "999",
            "profile": "h1",
            "protocol": "beradio2",
            "network": "696e4192-707f-4e8e-9246-78f6b41a280f",
            "gateway": "3756780977880301569"
        },
        "data": {
            "wght1": 106.77,
            "hum1": 488.0,
            "hum2": 572.0,
            "temp1": 21.63,
            "temp2": 19.25,
            "temp3": 10.92,
            "temp4": 13.54
        }
    }

.. note::

    You will see different values for ``meta.network`` and ``meta.gateway``, since they will be unique to your setup
    and are generated once.

    After being generated at the time of first invocation of ``beradio``, they are stored persistently on disk::

        Linux:   /home/he-devs/.local/share/beradio/config.json
        Mac OSX: /Users/amo/Library/Application Support/beradio/config.json
        Windows: unknown


Send BERadio messages
---------------------

Send random BERadio version 2 messages to the testing channel (network=test) on ``swarm.hiveeyes.org``::

    watch -n0.5 make pretend-swarm-random
