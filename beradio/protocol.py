# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import types
import bencode
from collections import OrderedDict

class BencodeError(Exception):
    pass

class BERadioProtocolBase(object):

    VERSION = None

    @classmethod
    def encode_ether(cls, data):
        payload = bencode.bencode(data)
        return payload

    @classmethod
    def decode_ether(cls, payload):

        # sanitize raw input payload
        payload = cls.sanitize(payload)

        # decode from Bencode format
        try:
            data = bencode.bdecode(payload)

        except bencode.BTL.BTFailure as ex:
            raise BencodeError(cls.failmsg(ex, payload))

        return data

    @classmethod
    def sanitize(cls, payload):
        # sanitize raw input payload
        return payload.strip('\0\r\n ')

    @classmethod
    def failmsg(cls, exception, payload):
        msg = 'ERROR: Decoding BERadio version {} data "{}" failed: {}'.format(cls.VERSION, payload, exception)
        print >>sys.stderr, msg
        return msg

    @classmethod
    def decode_safe(cls, payload):
        try:
            return cls.decode(payload)
        except Exception as ex:
            msg = cls.failmsg(ex, payload)
            raise


class BERadioProtocol1(BERadioProtocolBase):

    """
    Example payload::

        li999ei99ei1ei2218ei2318ei2462ei2250ee

    Decoded::

        [999, 99, 1, 2218, 2318, 2462, 2250]

    Mapped::

        {
            "network_id": 999,
            "node_id": 99,
            "gateway_id": 1,
            "temp1": 22.18,
            "temp2": 23.18,
            "temp3": 24.62,
            "temp4": 22.5
        }

    """

    VERSION = 1

    # "Bencode-over-Radio" aka. BERadio version 1 field names, order matters.
    # implicitly establishes struct-mapping while decoding raw payloads.
    fieldnames = [
        'network_id', 'node_id', 'gateway_id',
        'temp1', 'temp2', 'temp3', 'temp4',
    ]

    @classmethod
    def decode(cls, payload):

        data = cls.decode_ether(payload)

        # debug: output decoded data to stdout
        print 'message v1:', data

        assert type(data) is types.ListType, 'Data payload is not a list'

        # decode single values
        #network_id, node_id, gateway_id, temp1, temp2, temp3, temp4 = data
        response = OrderedDict()
        for name, value in zip(cls.fieldnames, data):

            # apply inverse scaling
            if name.startswith('temp'):
                value = float(value) / 100

            response[name] = value

        return response


class BERadioProtocol2(BERadioProtocolBase):

    """
    Example payload::

        d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee

    Decoded::

        {'h': [890, 377], 't': [3455, 3455, 3455, 3455], 'w': 12333}

    Mapped::

        {
            "hum1": 8.9,
            "hum2": 3.77,
            "temp1": 34.55,
            "temp2": 34.55,
            "temp3": 34.55,
            "temp4": 34.55,
            "wght1": 123.33
        }

    """

    VERSION = 2

    # dirty hack, since gateway_id is not published trough node anymore
    network_id = 999
    gateway_id = 1
    node_id = 99

    # BERadio version 2 sensor group identifiers
    # - Expand short names, e.g. "t" to "temp"
    # - Automatically enumerate multiple values and compute appropriate names, e.g. "temp1", "temp2", etc.
    # - Apply proper inverse scaling of sensor values
    identifiers = {
        't': { 'name': 'temp',   'scale': lambda x: float(x) / 100 },
        'h': { 'name': 'hum',    'scale': lambda x: float(x) / 1   },
        'w': { 'name': 'wght',   'scale': lambda x: float(x) / 100 },
        '_': { 'name': 'profile', 'attname' : 'direct'},
        '#': { 'name': 'nodeid',  'attname' : 'direct'},
    }

    @classmethod
    def decode(cls, payload):

        data = cls.decode_ether(payload)

        # debug: output decoded data to stdout
        print 'message v2:', data

        assert type(data) is types.DictType, 'Data payload is not a dictionary'

        # decode entries with nested lists for multiple entries
        response = OrderedDict()
        for identifier, value in data.iteritems():

            name = identifier
            if identifier in cls.identifiers:
                rule = cls.identifiers.get(identifier)
                name = rule.get('name', identifier)

                # list of values
                name_prefix = name
                if type(value) is types.ListType:
                    for idx, item in enumerate(value):
                        name = name_prefix + str(idx + 1)
                        if 'scale' in rule:
                            item = rule['scale'](item)
                        response[name] = item

                # scalar
                else:
                    if 'scale' in rule:
                        value = rule['scale'](value)
                    if 'attname' in rule and rule['attname'] == 'direct':
                        pass
                    else:
                        name += '1'

                    response[name] = value

        # backwards compatibility for upstream
        response.setdefault('network_id', cls.network_id)
        response.setdefault('gateway_id', cls.gateway_id)
        response.setdefault('node_id', cls.node_id)

        return response


def get_protocol_class(version):
    version = str(version)
    if version == '1':
        return BERadioProtocol1
    elif version == '2':
        return BERadioProtocol2
    else:
        return BERadioProtocol2
