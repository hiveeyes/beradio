#####################
BERadioMessageDecoder
#####################


************
Introduction
************
The `BERadio C++`_ encoder library provides automatic message fragmentation
yielding self-contained messages fitting into a defined maximum payload size.
Its default setting is ``MTU_SIZE_MAX 61``, making it suitable for typical ISM
applications.

The ``BERadioMessageDecoder`` is a decoder machinery for reassembling
fragmented BERadio messages into whole packets.

It works by waiting for a defined amount of time for new messages arriving.
Its default setting is ``REASSEMBLY_TIMEOUT = 2.5``, making it suitable to
reassemble messages spread across this time window into compound data packages.
After the defined time, ``BERadioMessageDecoder`` will release these
data packages for consumption by downstream software components.

.. _BERadio C++: https://hiveeyes.org/docs/arduino/BERadio/README.html



*************
Demonstration
*************
Let's show the functionality of the proof-of-concept.

.. highlight:: python


BERadio messages
================

Let's pretend there are four messages in flight:

- Three message fragments will arrive from node 2 containing values
  from a temperature array (temp1-5), two weight values (wght1-2),
  a single one for each humidity (hum1) and rssi (rssi1) and one
  cpu cycle counter (loop1).
- There's another message from node 3 containing values for
  temp1, hum1 and wght1.

Let's define these messages::

    >>> messages = [
    ...     'd1:#i2e1:_2:h11:tli2168ei1393ei3356ei1468ei1700ee1:hlee',
    ...     'd1:#i2e1:_2:h12:h0li8370ee1:wli53503600ei2590ee1:lli15100eee',
    ...     'd1:#i3e1:_2:h11:tli2168ee2:h0li930ee1:wli4242eee',
    ...     'd1:#i2e1:_2:h11:rli-6600eee',
    ... ]

Decoding the first message is easy and will get you an
understanding about what's actually inside::

    >>> from beradio.message import BERadioMessage
    >>> print(BERadioMessage.json(str(messages[0])))         # doctest: +ELLIPSIS
    {
        "data": {
            "temp1": 21.68,
            "temp2": 13.93,
            "temp3": 33.56,
            "temp4": 14.68,
            "temp5": 17.0
        },
        "meta": {
            "gateway": "None",
            "network": "None",
            "node": "2",
            "profile": "h1",
            "protocol": "beradio2",
            "time": ...
        }
    }


Setup machinery
===============

.. testsetup::

    >>> import time

Import the decoder module

    >>> from beradio.message import BERadioMessageDecoder

and make an instance of it

    >>> decoder = BERadioMessageDecoder()


Getting started
===============
Let's stuff the first two messages into the decoder,
simulating a transmission delay after each one:

    >>> decoder.read(messages[0])
    >>> time.sleep(0.5)

    >>> decoder.read(messages[1])
    >>> time.sleep(0.5)

Let's just stuff the remaining two messages into the decoder quickly to reduce runtime:

    >>> decoder.read(messages[2])
    >>> decoder.read(messages[3])


Reassembly
==========
After reassembling, all the data received during the default
time window of 2.5 seconds will be available as a whole bunch,
keyed by node id. Enjoy:

    >>> print(decoder.to_json())
    {
        "2": {
            "data": {
                "hum1": 83.7,
                "loops1": 151.0,
                "rssi1": -66.0,
                "temp1": 21.68,
                "temp2": 13.93,
                "temp3": 33.56,
                "temp4": 14.68,
                "temp5": 17.0,
                "wght1": 535036.0,
                "wght2": 25.9
            },
            "messages": [
                "d1:#i2e1:_2:h11:tli2168ei1393ei3356ei1468ei1700ee1:hlee",
                "d1:#i2e1:_2:h12:h0li8370ee1:wli53503600ei2590ee1:lli15100eee",
                "d1:#i2e1:_2:h11:rli-6600eee"
            ],
            "meta": {
                "gateway": "None",
                "network": "None",
                "node": "2",
                "profile": "h1",
                "protocol": "beradio2",
                "time": ...
            }
        },
        "3": {
            "data": {
                "hum1": 9.3,
                "temp1": 21.68,
                "wght1": 42.42
            },
            "messages": [
                "d1:#i3e1:_2:h11:tli2168ee2:h0li930ee1:wli4242eee"
            ],
            "meta": {
                "gateway": "None",
                "network": "None",
                "node": "3",
                "profile": "h1",
                "protocol": "beradio2",
                "time": ...
            }
        }
    }
