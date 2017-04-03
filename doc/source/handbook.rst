.. include:: links.rst

.. _beradio-python:

.. _handbook:

********
Handbook
********

.. contents::
   :local:
   :depth: 2

----

Quickstart
==========

Setup
-----
See :ref:`beradio-setup`.

Run forwarder
-------------

Read BERadio messages from serial interface and forward them to the specified MQTT broker::

    beradio forward --source=serial:///dev/ttyUSB0 --target='mqtt://username:password@mqtt.example.org'

Run dry-dock publisher
----------------------
For testing things in dry dock without a serial interface available,
we have to pretend. This is easy, we can just send data from the command line.
To get an idea about what's possible, please have a look at the ``Makefile``.

Publish multiple measurements as JSON::

    beradio forward --source='data://json:{"node": 42, "temperature": 42.84, "humidity": 83}' --target='mqtt://username:password@mqtt.example.org'

Publish multiple measurements as BERadio::

    beradio forward --source='data://d1:#i42e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee' --target='mqtt://username:password@mqtt.example.org'

Publish waveform data::

    beradio forward --source='func:sine' --target='mqtt://username:password@mqtt.example.org'


Running ``beradio``
===================

On the first invocation, ``beradio`` generates your private network and gateway identifiers
in form of ``network_id`` and ``gateway_id``, which get stored persistently.

Display its contents::

    beradio info

It should emit something like::

    --------------------------------------------------
                      beradio 0.8.1
    --------------------------------------------------
    config file: /Users/amo/Library/Application Support/beradio/config.json
    network_id:  696e4192-707f-4e8e-9246-78f6b41a280f
    gateway_id:  tug22



.. _handbook-tools:

Tools
=====

Decode Bencode payloads
-----------------------

This just decodes from Bencode format::

    $ bdecode li999ei99ei1ei2218ei2318ei2462ei2250ee
    [999, 99, 1, 2218, 2318, 2462, 2250]

    $ bdecode d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee
    {'w': 10677, 'h': [488, 572], '#': 999, 't': [2163, 1925, 1092, 1354], '_': 'h1'}


Decode BERadio messages
-----------------------

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
            "gateway": "tug22"
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
    and are generated once. ``meta.network`` uses UUID4_, while ``meta.gateway`` uses a generator for producing
    random, pronounceable pseudo-words, called ``gibberish``.

    After being generated at the time of first invocation of ``beradio``, they are stored persistently on disk::

        Linux:   /home/he-devs/.local/share/beradio/config.json
        Mac OSX: /Users/amo/Library/Application Support/beradio/config.json
        Windows: unknown


Shortcuts
=========

Run forwarder
-------------

Read BERadio messages from serial interface and forward them to a MQTT broker running on the same machine::

    make forward

Run dry-dock publisher
----------------------
For testing things in dry dock without a serial interface available,
we have to pretend. This is easy, we can just send data from the command line.
To get an idea about what's possible, please have a look at the ``Makefile``.

Publish multiple measurements::

    make publish-local data='json:{"temperature": 42.84, "humidity": 83}'

Publish single measurement::

    make publish-local data='value:{"volume": 72}'

Publish waveform data::

    make publish-local-func func=sine


Send BERadio messages
---------------------

For various examples, please have a look at the Makefile.

Send random BERadio version 2 messages to a MQTT broker running on localhost::

    make publish-local-func func=sine



.. _bemqtt:

Receive BERadio messages
------------------------

``bemqtt`` is a basic but convenient MQTT subscriber for setup, testing and debugging.

Subscribe to the catch-all MQTT topic of the total ``hiveeyes`` realm::

    bemqtt subscribe --source=mqtt://localhost

Subscribe to messages of a specific network::

    bemqtt subscribe 696e4192-707f-4e8e-9246-78f6b41a280f --source=mqtt://localhost

Subscribe to values of a single sensor::

    bemqtt subscribe 696e4192-707f-4e8e-9246-78f6b41a280f/tug22/999/temp1 --source=mqtt://localhost

