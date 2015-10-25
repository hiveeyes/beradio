.. _beradio-spec:

=====================
BERadio specification
=====================

:Version: 2.0.0
:Status: Work In Progress
:Date: 2015-10-17 to 2015-10-25

*BERadio* is ``Bencode-over-Radio``, a specification and reference implementation. Furthermore a neologism
from the infinite work-in-progress at the new Berlin airport *BER* - and the dalmatian word for *bye*, called *Adio*.

:Author: Richard Pobering <einsiedlerkrebs@ginnungagap.org>
:Author: Andreas Motl <andreas.motl@elmyra.de>


Scope
=====
This document defines the scope of the *BERadio* protocol naming-, decoding- and transformation-rules.
In general, this is about the "how" to ingest, map and transform messages in Bencode format and publish them to a MQTT bus.
The document still lacks formal language, so the concepts will be explained by examples.

Version 2
=========

BERadio version 2 uses a dictionary and nested lists for efficiently transmitting
multiple values from sensors of the same kind (e.g. 4 temperature sensors),
without wasting space on sending four almost identical attribute names (temp1, temp2, temp3, temp4).

To get an idea how things are translated, let's assume we receive this message over the air,
encoded using ``Bencode`` format::

    d2:h11:ni2e1:tli3455ei3455ei3455ei3455ee1:hli890ei377eee

This will get decoded into::

    {'h': [890, 377], '#': 2, 't': [3455, 3455, 3455, 3455], '_': 'h1'}

which will get translated into these distinct MQTT messages::

    hiveeyes/999/1/99/hum1     		8.9
    hiveeyes/999/1/99/hum2     		3.77
    hiveeyes/999/1/99/nodeid   		2
    hiveeyes/999/1/99/temp1   		34.55
    hiveeyes/999/1/99/temp2   		34.55
    hiveeyes/999/1/99/temp3   		34.55 
    hiveeyes/999/1/99/temp4		    34.55 
    hiveeyes/999/1/99/profile		h1  	# the profile could be changed for an alternative bunch of topics
    hiveeyes/999/1/99/network_id 	999 	#these value is hardcoded for now
    hiveeyes/999/1/99/gateway_id 	1   	#these value is hardcoded for now
    hiveeyes/999/1/99/node_id		99  	#these value is hardcoded for now
    hiveeyes/999/1/99/message-json {"hum1": 4.88, "hum2": 5.72, "temp1": 21.63, "temp2": 19.25, "temp3": 10.92, "temp4": 13.54, "wght1": 106.77, "network_id": 999, "gateway_id": 1, "node_id": 99} 
    hiveeyes/999/1/99/message-bencode d1:_2:h11:#i2e1:tli3455ei3455ei3455ei3455ee1:hli890ei377eee



The redundant transfer is justified by satisfying two contradicting requirements:

- Data should have the discrete value published to a specific topic in order to let generic devices subscribe to the raw sensor value. Example::

    hiveeyes/999/1/99/temp1             21.63

- Data should be sent blockwise in messages in order to make mapping, forwarding and storing more straight-forward. Example::

    hiveeyes/999/1/99/message-json      {"hum1": 8.9, "hum2": 3.77, "nodeid": 2, "temp1": 34.55, "temp2": 34.55, "temp3": 34.55, "temp4": 34.55, "profile": "h1", "network_id": 999, "gateway_id": 1, "node_id": 99}}

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
   _ for BERadio profile
   # for nodeid


Version 2.1
-----------

.. note::

    Future improvements, not implemented yet.

For discussion:
If it seems necessary Version 2.1 could take another hierarchical step deeper.
With that improvement it might become more generic. The question would be, if
we can support enough possible devices with BERadio v2 or if we might need
more since there are many e.g. temp sensors out there. We might want to get as
much data from the nodes as we can get. The payload limit is reached already so
we have to build different types of message subjects, e.g. vital data,
infrastructural, Weather and so on.

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
