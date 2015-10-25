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
    make forward-swarm-v2

    # read from serial interface, publish data
    # to a MQTT broker running on localhost
    make forward-v2

    # publish fixed Bencode payload to MQTT broker running on localhost, with network_id=999
    make pretend-local-v2

    # publish random data to ``swarm.hiveeyes.org``, with network_id=999
    make pretend-swarm-random-v2


On lab gateway using ``tmux``
-----------------------------
Run ``beradio`` forwarder on Raspberry Pi inside ``tmux``::

    # login and prepare tmux session
    ssh -p 222 he-devs@einsiedlerkrebs.ddns.net
    tmux new -s beradio

    # wo d' musi spuit
    cd ~/hiveeyes/beradio

    # start forwarder
    make forward-swarm-v2

    # quick mode does not work, this would close the tmux session when hitting CTRL+C
    #tmux new -s beradio 'bash -c "cd /home/he-devs/hiveeyes/beradio; make forward-swarm-v2; exec bash"'

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

    $ bdecode d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee
    {'h': [890, 377], 't': [3455, 3455, 3455, 3455], 'w': 12333}


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

    $ beradio decode d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee --protocol=2
    message v2: {'h': [890, 377], 't': [3455, 3455, 3455, 3455], 'w': 12333}
    {
        "hum1": 8.9,
        "hum2": 3.77,
        "temp1": 34.55,
        "temp2": 34.55,
        "temp3": 34.55,
        "temp4": 34.55,
        "wght1": 123.33
    }


Send BERadio messages
---------------------

Send random BERadio version 2 messages to the testing channel (network_id=999) on ``swarm.hiveeyes.org``::

    watch -n0.5 make pretend-swarm-random-v2
