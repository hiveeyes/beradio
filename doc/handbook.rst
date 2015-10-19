=======================
serial-to-mqtt handbook
=======================

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
