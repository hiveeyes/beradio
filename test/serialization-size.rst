.. include:: ../links.rst

.. _serialization-size-comparison:

########################
Serialization efficiency
########################
This compares space efficiency between different serialization formats.

.. contents::
   :local:
   :depth: 2

----

*********
Workbench
*********

.. testsetup::

    >>> from pprint import pprint

Setup
=====
Let's define a standard message payload::

    >>> payload = {'#': 999,
    ...            '_': 'h1',
    ...            'h1': 488.0,
    ...            'h2': 572.0,
    ...            't1': 21.63,
    ...            't2': 19.25,
    ...            't3': 10.92,
    ...            't4': 13.54,
    ...            'w1': 106.77}



Shootout
========

Unqualified
-----------

When not sending any key/attribute information, we gain a maximum of space efficiency,
but lose schema information completely. So the receiver must perfectly know about the
values we are sending. We almost can't leave out or add new values.

Binary
~~~~~~
Binary encoding is obviously on top of the list regarding payload size.
::

    >>> import struct
    >>> payload_binary = struct.pack(
    ...     '!Iccfffffff',
    ...     payload['#'],  payload['_'][0], payload['_'][1],
    ...     payload['t1'], payload['t2'],   payload['t3'], payload['t4'],
    ...     payload['h1'], payload['h2'],
    ...     payload['w1'])
    >>> payload_binary
    '\x00\x00\x03\xe7h1A\xad\n=A\x9a\x00\x00A.\xb8RAX\xa3\xd7C\xf4\x00\x00D\x0f\x00\x00B\xd5\x8a='
    >>> len(payload_binary)
    34

.. seealso:: https://docs.python.org/2/library/struct.html


CSVp
~~~~
The plain version of CSV. Just magic values.
::

    >>> payload_values = [str(value) for value in payload.values()]
    >>> payload_csv = ','.join(payload_values)
    >>> payload_csv
    '999,106.77,572.0,13.54,488.0,19.25,10.92,h1,21.63'
    >>> len(payload_csv)
    49


Qualified
---------

When sending at least a single-letter identifier describing the sensor (values),
we can deduce a lot more information from the message payload.


BERadio
~~~~~~~
*BERadio* applies scaling to get rid of float values, single-item compression and encodes the *nodeid* as integer.
It has knowledge about how to apply different scalings and conversions by incorporating *profiles* to avoid sending
unencodable types, e.g. floats.

It is the clear winner of encodings retaining readability through staying ASCII
while still including key/attribute information.

Build message::

    >>> from beradio.message import BERadioMessage
    >>> message = BERadioMessage(999)
    >>> message.temperature(21.63, 19.25, 10.92, 13.54)
    >>> message.humidity(488.0, 572.0)
    >>> message.weight(106.77)

Serialize message::

    >>> str(message)
    'd1:#i999e1:_2:h11:hli48800ei57200ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee'
    >>> len(str(message))
    75


CSVq
~~~~
A qualified version of CSV. Prefixes items with shortcut attribute name.
::

    >>> entries = [key + ':' + str(value) for key, value in payload.iteritems()]
    >>> payload_csv = ','.join(entries)
    >>> payload_csv
    '#:999,w1:106.77,h2:572.0,t4:13.54,h1:488.0,t2:19.25,t3:10.92,_:h1,t1:21.63'
    >>> len(payload_csv)
    74


Bencode
~~~~~~~
Unfortunately, Bencode can not encode float values::

    >>> import bencode
    >>> len(bencode.bencode(payload))
    Traceback (most recent call last):
      File "bencode/__init__.py", line 110, in encode_dict
        encode_func[type(v)](v, r)
    KeyError: <type 'float'>

After converting to int values with uniform scaling::

    >>> payload_integers = dict([key, int(value * 100) if type(value) is float else value] for key, value in payload.iteritems())
    >>> message = bencode.bencode(payload_integers)
    >>> message
    'd1:#i999e1:_2:h12:h1i48800e2:h2i57200e2:t1i2163e2:t2i1925e2:t3i1092e2:t4i1354e2:w1i10677ee'
    >>> len(message)
    90


YAML
~~~~
::

    >>> import yaml
    >>> message = yaml.dump(payload)
    >>> message
    "{'#': 999, _: h1, h1: 488.0, h2: 572.0, t1: 21.63, t2: 19.25, t3: 10.92, t4: 13.54,\n  w1: 106.77}\n"
    >>> len(message)
    98


MessagePack
~~~~~~~~~~~
http://msgpack.org/
::

    >>> import umsgpack
    >>> message = umsgpack.dumps(payload)
    >>> message
    '\x89\xc4\x01#\xcd\x03\xe7\xc4\x02w1\xcb@Z\xb1G\xae\x14z\xe1\xc4\x02h2\xcb@\x81\xe0\x00\x00\x00\x00\x00\xc4\x02t4\xcb@+\x14z\xe1G\xae\x14\xc4\x02h1\xcb@~\x80\x00\x00\x00\x00\x00\xc4\x02t2\xcb@3@\x00\x00\x00\x00\x00\xc4\x02t3\xcb@%\xd7\n=p\xa3\xd7\xc4\x01_\xc4\x02h1\xc4\x02t1\xcb@5\xa1G\xae\x14z\xe1'
    >>> len(message)
    105


JSON
~~~~
::

    >>> import json
    >>> message = json.dumps(payload)
    >>> message
    '{"#": 999, "w1": 106.77, "h2": 572.0, "t4": 13.54, "h1": 488.0, "t2": 19.25, "t3": 10.92, "_": "h1", "t1": 21.63}'
    >>> len(message)
    113



*******
Outlook
*******

Marshallers suitable for embedded use
=====================================

Classic
-------
- | Nanopb: protocol buffers with small code size
  | https://koti.kapsi.fi/jpa/nanopb/
- | BSON: Binary JSON, a binary-encoded serialization of JSON-like documents
  | http://bsonspec.org/
- | CBOR: Concise Binary Object Representation
  | https://tools.ietf.org/html/rfc7049
- | SenML (see TODO.rst)

Modern
------
From some discussion about the article `RFM69 to MQTT gateway using ESP8266`_
on `Martin Harizanov`_'s weblog, we should follow to the article
`Serializing data from IoT nodes`_ by `Johan Kanflo`_.
It greatly reflects the zeitgeist and also has pointers to

- SMILE_, a binary serialization of generic JSON data model and
- UBJSON_ (`UBJSON at Wikipedia`_), "the universally compatible format specification for binary JSON".


Other marshallers
=================
- Protocol Buffers
- Thrift
- Avro
- | Capnproto
  | https://capnproto.org/
- Gob
   * https://blog.golang.org/gobs-of-data
   * https://golang.org/pkg/encoding/gob/
   * https://play.golang.org/p/_-OJV-rwMq


Compression
===========
For reducing payload size, there's also compression, which might come handy.

- | zlib
  | http://www.zlib.net/
- | LZ4
  | https://cyan4973.github.io/lz4/
  | https://github.com/Cyan4973/lz4

