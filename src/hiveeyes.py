# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import bencode
from collections import OrderedDict

class HiveeyesWireProtocol(object):

    fieldnames = [
        'network_id', 'node_id', 'gateway_id',
        'temp1', 'temp2', 'temp3', 'temp4',
    ]

    @classmethod
    def encode(cls, data):
        payload = bencode.bencode(data)
        return payload

    @classmethod
    def sanitize(cls, payload):
        # sanitize raw input payload
        return payload.strip('\0\r\n ')

    @classmethod
    def decode(cls, payload):

        # sanitize raw input payload
        data_raw = cls.sanitize(payload)

        # decode from Bencode format
        try:
            data = bencode.bdecode(data_raw)

        except bencode.BTL.BTFailure as ex:
            print 'ERROR: Could not decode Bencode payload "{}": {}'.format(data_raw, ex)
            return

        # debug: output decoded data to stdout
        #print 'data:', data

        # decode single values
        #network_id, node_id, gateway_id, temp1, temp2, temp3, temp4 = data
        response = OrderedDict()
        for name, value in zip(cls.fieldnames, data):

            # apply inverse scaling
            if name.startswith('temp'):
                value = float(value) / 100

            response[name] = value

        return response


class HiveeyesPublisher(object):

    def __init__(self, channel):
        self.channel = channel

    def publish(self, payload, data):

        # publish to different topics
        self.channel.publish_field(data, 'temp1')
        self.channel.publish_field(data, 'temp2')
        self.channel.publish_field(data, 'temp3')
        self.channel.publish_field(data, 'temp4')

        # publish en-bloc
        self.channel.publish_scalar(data, 'message-bencode', payload)
        self.channel.publish_json(data, 'message-json', data)
