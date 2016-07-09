=============
BERadio tests
=============

.. testsetup::

    >>> from pprint import pprint

BERadioMessage
==============

The most convenient interface on API level.

Import module::

    >>> from beradio.message import BERadioMessage

Construct message with nodeid=999::

    >>> message = BERadioMessage(999)

Fill with data::

    >>> message.temperature(21.63, 19.25, 10.92, 13.54)
    >>> message.humidity(488.0, 572.0)
    >>> message.weight(106.77)

Encode the message to wire format::

    >>> str(message)
    'd1:#i999e1:_2:h11:hli48800ei57200ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee'

Decode back::

    >>> pprint(BERadioMessage.decode(str(message)))         # doctest: +ELLIPSIS
    {'data': {'hum1': 488.0,
              'hum2': 572.0,
              'temp1': 21.63,
              'temp2': 19.25,
              'temp3': 10.92,
              'temp4': 13.54,
              'wght1': 106.77},
     'meta': {'gateway': 'None',
              'network': 'None',
              'node': '999',
              'profile': 'h1',
              'protocol': 'beradio2',
              'time': ...}}


Construct small messages on purpose
-----------------------------------

Construct and fill message::

    >>> message = BERadioMessage(999)
    >>> message.temperature(21.63, 19.25)
    >>> message.weight(106.77)

Show what's up::

    >>> str(message)
    'd1:#i999e1:_2:h11:tli2163ei1925ee1:wi10677ee'
    >>> len(str(message))
    44

Decode back::

    >>> pprint(BERadioMessage.decode(str(message)))         # doctest: +ELLIPSIS
    {'data': {'temp1': 21.63, 'temp2': 19.25, 'wght1': 106.77},
     'meta': {'gateway': 'None',
              'network': 'None',
              'node': '999',
              'profile': 'h1',
              'protocol': 'beradio2',
              'time': ...}}


Decode message fragments
------------------------
Apply list continuation by honoring index offsets encoded after family identifier.

Define message::

    >>> message = 'd1:#i2e1:_2:h12:t6li8484ei2121ee1:hli5000ei5500ei7710eee'


Decode message::

    >>> pprint(BERadioMessage.decode(str(message)))         # doctest: +ELLIPSIS
    {'data': {'hum1': 50.0,
              'hum2': 55.0,
              'hum3': 77.1,
              'temp7': 84.84,
              'temp8': 21.21},
     'meta': {'gateway': 'None',
              'network': 'None',
              'node': '2',
              'profile': 'h1',
              'protocol': 'beradio2',
              'time': ...}}

