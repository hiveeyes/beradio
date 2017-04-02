.. _beradio-spec:

=====================
BERadio specification
=====================

:Version: 2.0.0
:Status: Work In Progress
:Date: 2015-10-17 to 2015-10-25

*BERadio* is ``Bencode-over-Radio``, a specification and reference implementation. Furthermore a neologism
from the infinite work-in-progress at the new Berlin airport *BER* - and the dalmatian word for *bye*, called *Adio*.

:Author: Richard Pobering <richard@hiveeyes.org>
:Author: Andreas Motl <andreas@hiveeyes.org>


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
encoded using *Bencode* format::

    d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee

Decoding it from *Bencode* gives::

    {'#': 999, '_': 'h1', 't': [2163, 1925, 1092, 1354], 'h': [488, 572], 'w': 10677}

Further applying *BERadio* protocol decoding, this will yield (slightly formatted for better readability)::

    {
        "meta": {
            "protocol": "beradio2",
            "network":  "{network}",
            "gateway":  "{gateway}",
            "node":     "999",
            "profile":  "h1",
        },
        "data": {
            "temp1":  21.63,
            "temp2":  19.25,
            "temp3":  10.92,
            "temp4":  13.54
            "hum1":  488.0,
            "hum2":  572.0,
            "wght1": 106.77,
        }
    }

Finally, when forwarding this message to MQTT, it will get translated into these distinct MQTT message publications::

    hiveeyes/{network}/{gateway}/999/temp1             21.63
    hiveeyes/{network}/{gateway}/999/temp2             19.25
    hiveeyes/{network}/{gateway}/999/temp3             10.92
    hiveeyes/{network}/{gateway}/999/temp4             13.54
    hiveeyes/{network}/{gateway}/999/hum1              488.0
    hiveeyes/{network}/{gateway}/999/hum2              572.0
    hiveeyes/{network}/{gateway}/999/wght1             106.77
    hiveeyes/{network}/{gateway}/999/message-json      {"temp1": 21.63, "temp2": 19.25, "temp3": 10.92, "temp4": 13.54, "hum1": 488.0, "hum2": 572.0, "wght1": 106.77}
    hiveeyes/{network}/{gateway}/999/message-bencode   d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee

.. note::

    The identifier placeholders above are populated using UUID4 and Snowflake id generation algorithms::

        {network}: 696e4192-707f-4e8e-9246-78f6b41a280f
        {gateway}: tug22


The redundant transfer is justified by satisfying two contradicting requirements:

- Data should have the discrete value published to a specific topic in order to let generic devices subscribe to the raw sensor value. Example::

    hiveeyes/696e4192-707f-4e8e-9246-78f6b41a280f/tug22/999/temp1             21.63

- Data should be sent blockwise in messages in order to make mapping, forwarding and storing more straight-forward. Example::

    hiveeyes/696e4192-707f-4e8e-9246-78f6b41a280f/tug22/999/message-json      {"temp1": 21.63, "temp2": 19.25, "temp3": 10.92, "temp4": 13.54, "hum1": 488.0, "hum2": 572.0, "wght1": 106.77}

  This format-style requires little efforts on the receiver side in order to store that measurement point directly into the database.


.. note::

    The ``beradio`` Python distribution provides convenient commandline-based decoding tools for working with
    messages in *Bencode* and *BERadio* formats, called ``bdecode`` and ``beradio decode``. For more information,
    consider reading about :ref:`BERadio Tools <handbook-tools>`.



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

.. note::

    Write some more words about the fact that the node id is encoded as integer on the air while it is forwarded as
    string on the upstream network.

Version 2.1
-----------

.. warning::

    Future improvements, not implemented yet.

Named Scaling
~~~~~~~~~~~~~
To improve the profile building it should be implemented a function which allows named scaling.
The idea behind is, that you could use a scaling factor defined in the specification and have it accessible
in the rule descriptions through a named label.

Fragmentation and Reassembly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fragmentation an the node-side, which takes care of the maximum payload size and build the Bencoded message.

Scheduler
~~~~~~~~~
A scheduler which allows not to send all data at every time. Maybe infrastructural data twice a day and vital data much more often.

Convenient C++ library ``libberadio``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Build a C-struct which takes care of the maximal payload and is placeholder for all kinds values,
this struct is filled from the sensors files the message together with other the profile and the
nodeid and is send, afterwards the values are nulled.

TBD
~~~
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
