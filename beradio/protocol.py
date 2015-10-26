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
    fieldnames_meta = [
        'network_id', 'node_id', 'gateway_id',
    ]
    fieldnames_data = [
        'temp1', 'temp2', 'temp3', 'temp4',
    ]
    fieldnames = fieldnames_meta + fieldnames_data

    @classmethod
    def decode(cls, payload):

        data = cls.decode_ether(payload)

        # debug: output decoded data to stdout
        print 'INFO:    message v1:', data

        # sanity checks
        # TODO: check exception handling for AssertionError
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

    @classmethod
    def to_v2(cls, message1):
        message2 = {
            'meta': {
                'network': message1['network_id'],
                'gateway': message1['gateway_id'],
                'node': message1['node_id'],
            },
            'data': { key:value for key, value in message1.items() if key in cls.fieldnames_data }
        }
        return message2


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
    # TODO: network_id should be stored in configuration file
    # TODO: gateway_id should be stored in configuration file
    network_id = 'test'
    gateway_id = '1'

    # BERadio version 2 sensor group identifiers
    # - Expand short names, e.g. "t" to "temp"
    # - Automatically enumerate multiple values and compute appropriate names, e.g. "temp1", "temp2", etc.
    # - Apply proper inverse scaling of sensor values
    identifiers = {
        '#': { 'name': 'node',    'attname' : 'direct', 'meta': True, 'convert': str},
        '_': { 'name': 'profile', 'attname' : 'direct', 'meta': True, 'convert': str},
        't': { 'name': 'temp',    'scale': lambda x: float(x) / 100 },
        'h': { 'name': 'hum',     'scale': lambda x: float(x) / 1   },
        'w': { 'name': 'wght',    'scale': lambda x: float(x) / 100 },
    }

    @classmethod
    def decode(cls, payload):

        # decode data from air
        data_in = cls.decode_ether(payload)

        # debug: output decoded data to stdout
        print 'INFO:    message v2:', data_in

        # sanity checks
        # TODO: check exception handling for AssertionError
        assert type(data_in) is types.DictType, 'Data payload is not a dictionary'

        # prepare response structure
        response = {
            'meta': {
                'protocol': 'beradio2',
                'network': str(cls.network_id),
                'gateway': str(cls.gateway_id),
                'node': None,
            },
            'data': OrderedDict(),
        }

        # decode entries with nested lists for multiple entries
        for identifier, value in data_in.iteritems():

            if identifier in cls.identifiers:

                rule = cls.identifiers.get(identifier)
                name = rule.get('name', identifier)
                is_meta = rule.get('meta', False)

                response_key = 'meta' if is_meta else 'data'

                # list of values
                name_prefix = name
                if type(value) is types.ListType:
                    for idx, item in enumerate(value):
                        name = name_prefix + str(idx + 1)
                        item = cls.decode_value(item, rule)
                        response[response_key][name] = item

                # scalar
                else:
                    value = cls.decode_value(value, rule)

                    if 'attname' in rule and rule['attname'] == 'direct':
                        pass
                    else:
                        name += '1'

                    response[response_key][name] = value

        return response

    @classmethod
    def decode_value(cls, value, rule):
        if 'convert' in rule:
            value = rule['convert'](value)
        if 'scale' in rule:
            value = rule['scale'](value)
        return value

def get_protocol_class(version):
    version = str(version)
    if version == '1':
        return BERadioProtocol1
    elif version == '2':
        return BERadioProtocol2
    else:
        return BERadioProtocol2
