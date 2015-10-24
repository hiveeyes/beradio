=====================
BERadio specification
=====================

``BERadio`` is ``Bencode-over-Radio``. Furthermore a Neologism from the infite work
in progress Berlin Airport BER and the Dalmatian word für 'bye' Adio.

Intro
=====
By showing examples, this document currently defines the scope of
the ``BERadio`` protocol naming-, decoding- and transformation-rules.
It is about the "how" to ingest, map and transform messages in Bencode format and publish them to an MQTT bus.

TODO: What about other bus systems, like WAMP? See also https://github.com/goeddea/scratchbox/blob/master/yun/serial_to_wamp.js

Version 2
=========

BERadio version 2 uses a dictionary and nested lists for efficiently transmitting
multiple values from sensors of the same kind (e.g. 4 temperature sensors),
without wasting space on sending four almost identical attribute names (temp1, temp2, temp3, temp4).

To get an idea how things are translated, let's assume we receive this message over the air,
encoded using ``Bencode`` format::

    d1:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee

This will get decoded into::

    {'t': [2163, 1925, 1092, 1354], 'h': [488, 572], 'w': 10677}

which will get translated into these distinct MQTT messages::

    hiveeyes/999/1/99/temp1     21.63
    hiveeyes/999/1/99/temp2     19.25
    hiveeyes/999/1/99/temp3     10.92
    hiveeyes/999/1/99/temp4     13.54
    hiveeyes/999/1/99/hum1      4.88
    hiveeyes/999/1/99/hum2      5.72
    hiveeyes/999/1/99/wght1     106.77
    hiveeyes/999/1/99/message-json {"hum1": 4.88, "hum2": 5.72, "temp1": 21.63, "temp2": 19.25, "temp3": 10.92, "temp4": 13.54, "wght1": 106.77, "network_id": 999, "gateway_id": 1, "node_id": 99}
    hiveeyes/999/1/99/message-bencode d1:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee


The redundant transfer is justified by satisfying two contradicting requirements:

- Data should have the discrete value published to a specific topic in order to let generic devices subscribe to the raw sensor value. Example::

    hiveeyes/999/1/99/temp1             21.63

- Data should be sent blockwise in messages in order to make mapping, forwarding and storing more straight-forward. Example::

    hiveeyes/999/1/99/message-json      {"network_id": 999, "node_id": 99, "gateway_id": 1, "temp1": 21.63, "temp2": 19.25, "temp3": 10.92, "temp4": 13.54}

  After minor manipulation, this is stored directly into InfluxDB.

Specification
-------------

These are the ongoing specs for BERadio V2. So far it uses::

   Values are received without dots and will be added trough BERadio
   t for temp
      * 100
   h for humidity
      * ??
   w for weight
      * 1000?


Version 2.1
-----------

.. warning::

    Future improvements, not implemented yet.

For discussion:
If it seems necessary Version 2.1 could take another hierarchical step deeper.
With that improvement it might become more generic. The question would be, if
we can support enough possible devices with BERadio v2 or if we might need
more since there are many e.g. temp sensors out there. We might want to get as
much data from the nodes as we can get. The payload limit is reached already so
we have to build different types of message subjects, e.g. Vital Data,
Infrastructural, Weather and so on.

Specification
.............

These are the ongoing specs for BERadio V2. So far it uses:


In the 1st hierarchy the data Purpose is stored, it could be::

   v for vital data (e.G. data from within the hive)
   w for wheater information (Sensors outside the hive)
   i for infrastructural Data (e.G. RSSI Battery time)

alternatively or extra Device Specification::

   d dallas temperature Sensors


In the 2nd hierarchy we store values, which are received without dots and be added later on::

   t for temp
      * 100
   h for humidity
      * ??
   w for weight
      * 1000?


Version 1
=========

BEradio version 1 uses a list of unqualified items, the receiver must have the information about the field names
and how to apply reverse scaling. Think of CSV.

To get an idea how things are translated, let's assume we receive this message over the air,
encoded using ``Bencode`` format::

    li999ei99ei1ei2218ei2318ei2462ei2250ee

This will get decoded into::

    [999, 99, 1, 2218, 2318, 2462, 2250]

which will get translated into these distinct MQTT messages::

    hiveeyes/999/1/99/temp1             22.18
    hiveeyes/999/1/99/temp2             23.18
    hiveeyes/999/1/99/temp3             24.62
    hiveeyes/999/1/99/temp4             22.5
    hiveeyes/999/1/99/message-json      {"network_id": 999, "node_id": 99, "gateway_id": 1, "temp1": 22.18, "temp2": 23.18, "temp3": 24.62, "temp4": 22.5}
    hiveeyes/999/1/99/message-bencode   li999ei99ei1ei2218ei2318ei2462ei2250eei
