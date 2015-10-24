================
BERadio handbook
================


Decoding Bencode payloads
=========================

This just decodes from Bencode format::

    $ bdecode li999ei99ei1ei2218ei2318ei2462ei2250ee
    [999, 99, 1, 2218, 2318, 2462, 2250]

    $ bdecode d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee
    {'h': [890, 377], 't': [3455, 3455, 3455, 3455], 'w': 12333}


Decoding BERadio messages
=========================

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

Send random BERadio version 2 messages to the testing channel on ``swarm``::

    watch -n0.5 make pretend-swarm-random-v2


Running ``serial-to-mqtt``
==========================

Read the source, luke. A good starting point is the ``Makefile``, just follow along into ``src/publish.py`` and finally ``src/serial_to_mqtt.py``.

Run ``serial-to-mqtt`` forwarder on Raspberry Pi inside ``tmux``::

    # login and prepare tmux session
    ssh -p 222 he-devs@einsiedlerkrebs.ddns.net
    tmux new -s serial-to-mqtt

    # wo d' musi spuit
    cd ~/hiveeyes/serial-to-mqtt

    # read from serial interface, publish data directly to the central data collector on ``swarm.hiveeyes.org`` using MQTT
    make forward-swarm

    # read from serial interface, publish data directly to a MQTT broker running on localhost
    # TODO: to make this work end-to-end making data actually available in Grafana on swarm.hiveeyes.org, two Mosquittos have to talk to each other
    make forward

    # publish fixed Bencode payload to MQTT broker running on localhost, with network_id=999
    make pretend-local

    # publish random data to ``swarm.hiveeyes.org``, with network_id=999
    make pretend-swarm-random

Run forwarder inside new ``tmux`` session, quick::

    ssh -p 222 he-devs@einsiedlerkrebs.ddns.net
    tmux new -s serial-to-mqtt
    cd /home/he-devs/hiveeyes/serial-to-mqtt; make forward-swarm

    # does not work!
    #tmux new -s serial-to-mqtt 'bash -c "cd /home/he-devs/hiveeyes/serial-to-mqtt; make forward-swarm; exec bash"'


Attach to running instance
==========================
::

    # login and prepare tmux session
    ssh -p 222 he-devs@einsiedlerkrebs.ddns.net

    # attach to session
    tmux att -t serial-to-mqtt
