# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import bencode
from collections import OrderedDict


class BERadioProtocolBase(object):

    @classmethod
    def encode(cls, data):
        payload = bencode.bencode(data)
        return payload

    @classmethod
    def decode(cls, payload):

        # sanitize raw input payload
        payload = cls.sanitize(payload)

        # decode from Bencode format
        try:
            data = bencode.bdecode(payload)

        except bencode.BTL.BTFailure as ex:
            msg = 'ERROR: Decoding Bencode data "{}" failed: {}'.format(payload, ex)
            print >>sys.stderr, msg
            raise ValueError(msg)

        return data

    @classmethod
    def sanitize(cls, payload):
        # sanitize raw input payload
        return payload.strip('\0\r\n ')


class BERadioProtocol1(BERadioProtocolBase):

    VERSION = 1

    # "Bencode-over-Radio" field names, order matters.
    # implicitly establishes struct-mapping while decoding raw payloads.
    fieldnames = [
        'network_id', 'node_id', 'gateway_id',
        'temp1', 'temp2', 'temp3', 'temp4',
    ]

    @classmethod
    def decode(cls, payload):

        data = BERadioProtocolBase.decode(payload)

        # debug: output decoded data to stdout
        print 'data:', data

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

    VERSION = 2

    # "Bencode-over-Radio" field names, order matters.
    # implicitly establishes struct-mapping while decoding raw payloads.
    fieldnames = [
        'node_id', 'gateway_id',
        'temp1', 'temp2', 'temp3', 'temp4',
        'hum1', 'hum2',
        'wght1',
        ]

    # dirty hack, since gateway_id is not published trough node anymore
    gateway_id = 1

    @classmethod
    def decode(cls, payload):

        data = BERadioProtocolBase.decode(payload)

        # debug: output decoded data to stdout
        print 'data:', data

        # decode single values
        #network_id, node_id, gateway_id, temp1, temp2, temp3, temp4 = data
        response = OrderedDict()
        for name, value in zip(cls.fieldnames, data):

            # apply inverse scaling
            if name.startswith('temp'):
                value = float(value) / 100

            response[name] = value

        return response
