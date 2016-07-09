# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from pprint import pformat
from beradio.protocol import BERadioProtocol2

class BERadioMessage(object):

    protocol_factory = BERadioProtocol2

    def __init__(self, nodeid, profile='h1'):
        """
        >>> message = BERadioMessage(999)

        >>> str(message)
        'd1:#i999e1:_2:h1e'

        >>> message.temperature(21.63, 19.25, 10.92, 13.54)
        >>> str(message)
        'd1:#i999e1:_2:h11:tli2163ei1925ei1092ei1354eee'

        >>> message.humidity(488.0, 572.0)
        >>> str(message)
        'd1:#i999e1:_2:h11:hli48800ei57200ee1:tli2163ei1925ei1092ei1354eee'

        >>> message.weight(106.77)
        >>> str(message)
        'd1:#i999e1:_2:h11:hli48800ei57200ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee'

        """
        self.nodeid = int(nodeid)
        self.profile = str(profile)
        self.payload = {}
        self.protocol = self.protocol_factory()


    def temperature(self, *args):
        self.payload['t'] = self.protocol.encode_values('t', args)

    def humidity(self, *args):
        self.payload['h'] = self.protocol.encode_values('h', args)

    def weight(self, *args):
        self.payload['w'] = self.protocol.encode_values('w', args)

    def clear(self):
        self.payload = {}

    def encode(self):
        data = {
            '#': self.nodeid,
            '_': self.profile,
        }
        data.update(self.payload)
        message = self.protocol.encode_ether(data)
        return message

    def __str__(self):
        return self.encode()

    def __repr__(self):
        data = {
            '#': self.nodeid,
            '_': self.profile,
            }
        data.update(self.payload)
        return pformat(data)

    @classmethod
    def decode(cls, payload):
        message = cls.protocol_factory().decode(payload)
        message['data'] = dict(message['data'])
        return message
