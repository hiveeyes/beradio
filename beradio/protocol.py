# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015-2022 Andreas Motl <andreas@hiveeyes.org>
import logging
from collections import OrderedDict

import bencode

from .util import timestamp_nanos

logger = logging.getLogger(__name__)


class BencodeError(Exception):
    pass


class BERadioProtocolBase(object):

    VERSION = None

    def __init__(self, network_id=None, gateway_id=None):
        self.network_id = network_id
        self.gateway_id = gateway_id

    def encode_ether(self, data):
        """
        Encode proper data structure for sending over the air.
        This is just plain Bencode.

        >>> data = {
        ...     '#': 999,
        ...     '_': 'h1',
        ...     't': [2163, 1925, 1092, 1354],
        ...     'h': [488, 572],
        ...     'w': 10677
        ... }

        >>> BERadioProtocolBase().encode_ether(data)
        b'd1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee'
        """
        payload = bencode.bencode(data)
        return payload

    def decode_ether(self, payload):
        """
        Sanitize and decode from Bencode format.

        >>> BERadioProtocolBase().decode_ether('d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee\\0\\r\\n ')  # noqa:E501
        OrderedDict([('#', 999), ('_', 'h1'), ('h', [488, 572]), ('t', [2163, 1925, 1092, 1354]), ('w', 10677)])
        """

        # sanitize raw input payload
        payload = self.sanitize(payload)

        # decode from Bencode format
        try:
            data = bencode.bdecode(payload)

        except bencode.BTL.BTFailure as ex:
            raise BencodeError(self.failmsg(ex, payload))

        return data

    @staticmethod
    def sanitize(payload):
        """
        Sanitize raw input payload to make decoding not croak.

        >>> BERadioProtocolBase().sanitize('hello_message\\0\\r\\n ')
        b'hello_message'

        >>> BERadioProtocolBase().sanitize(b'hello_message\\0\\r\\n ')
        b'hello_message'
        """
        if isinstance(payload, str):
            payload = payload.encode()
        return payload.strip(b"\0\r\n ")

    def failmsg(self, exception, payload):
        msg = 'ERROR: Decoding BERadio version {} data "{}" failed: {}'.format(self.VERSION, payload, exception)
        logger.error(msg)
        return msg

    def decode(self, payload):
        """
        Decoding without implementation should raise an exception.

        >>> be = BERadioProtocolBase()
        >>> be.failmsg = lambda x, y: None
        >>> be.decode('hello_message\\0\\r\\n ')
        Traceback (most recent call last):
          File "beradio/protocol.py", line 89, in decode
            raise NotImplementedError('Please implement in inheriting class.')
        NotImplementedError: Please implement in inheriting class.
        """
        raise NotImplementedError("Please implement in inheriting class.")

    def decode_safe(self, payload):
        try:
            return self.decode(payload)
        except Exception as ex:
            raise BencodeError(self.failmsg(ex, payload))


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
        "network_id",
        "node_id",
        "gateway_id",
    ]
    fieldnames_data = [
        "temp1",
        "temp2",
        "temp3",
        "temp4",
    ]
    fieldnames = fieldnames_meta + fieldnames_data

    def decode(self, payload):

        data = self.decode_ether(payload)

        # debug: output decoded data to stdout
        logger.info("message v1: {}".format(data))

        # sanity checks
        # TODO: check exception handling for AssertionError
        assert isinstance(data, list), "Data payload is not a list"

        # decode single values
        # network_id, node_id, gateway_id, temp1, temp2, temp3, temp4 = data
        response = OrderedDict()
        for name, value in zip(self.fieldnames, data):

            # apply inverse scaling
            if name.startswith("temp"):
                value = float(value) / 100

            response[name] = value

        return response

    def to_v2(self, message1):
        message2 = {
            "meta": {
                "network": message1["network_id"],
                "gateway": message1["gateway_id"],
                "node": message1["node_id"],
            },
            "data": {key: value for key, value in message1.items() if key in self.fieldnames_data},
        }
        return message2


class BERadioProtocol2(BERadioProtocolBase):

    """
    Example payload::

        d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee

    Decoded::

        {'w': 10677, 'h': [488, 572], '#': 999, 't': [2163, 1925, 1092, 1354], '_': 'h1'}

    Mapped::

        {
            "meta": {
                "node": "999",
                "profile": "h1",
                "protocol": "beradio2",
                "network": "efc54ed2-b010-42ee-bfb6-183f148885f1",
                "gateway": "tug22"
            },
            "data": {
                "wght1": 106.77,
                "hum1": 488.0,
                "hum2": 572.0,
                "temp1": 21.63,
                "temp2": 19.25,
                "temp3": 10.92,
                "temp4": 13.54
            }
        }

    """

    VERSION = 2

    # BERadio version 2 sensor group identifiers
    # - Expand short names, e.g. "t" to "temp"
    # - Automatically enumerate multiple values and compute appropriate names, e.g. "temp1", "temp2", etc.
    # - Apply proper inverse scaling of sensor values
    identifiers = {
        "#": {"name": "node", "attname": "direct", "meta": True, "convert": str},
        "_": {"name": "profile", "attname": "direct", "meta": True, "convert": str},
        "t": {"name": "temp", "scale-encode": lambda x: int(x * 100), "scale-decode": lambda x: float(x) / 100},
        "h": {"name": "hum", "scale-encode": lambda x: int(x * 100), "scale-decode": lambda x: float(x) / 100},
        "w": {"name": "wght", "scale-encode": lambda x: int(x * 100), "scale-decode": lambda x: float(x) / 100},
        "r": {"name": "rssi", "scale-encode": lambda x: int(x * 100), "scale-decode": lambda x: float(x) / 100},
        "l": {"name": "loops", "scale-encode": lambda x: int(x * 100), "scale-decode": lambda x: float(x) / 100},
    }

    def get_envelope(self, node=None):

        # Create nanosecond timestamp
        # TODO: Make this only conditionally?
        timestamp = timestamp_nanos()

        # Prepare response structure
        response = {
            "meta": {
                "protocol": "beradio2",
                "network": str(self.network_id),
                "gateway": str(self.gateway_id),
                "node": str(node),
                "time": timestamp,
            },
            "data": OrderedDict(),
        }
        return response

    def decode(self, payload):
        """
        Decode BERadio2 message.

        >>> BERadioProtocol2().decode('d1:#i999e1:_2:h11:hli48800ei57200ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee\\0\\r\\n ')  # doctest:+ELLIPSIS, noqa:E501
        {'meta': {'protocol': 'beradio2', 'network': 'None', 'gateway': 'None', 'node': '999', 'time': ..., 'profile': 'h1'}, 'data': OrderedDict([('hum1', 488.0), ('hum2', 572.0), ('temp1', 21.63), ('temp2', 19.25), ('temp3', 10.92), ('temp4', 13.54), ('wght1', 106.77)])}  # noqa:E501
        """

        # Decode data from air
        data_in = self.decode_ether(payload)

        # Debugging: Display decoded data on STDOUT
        logger.debug("message v2: {}".format(data_in))

        # Sanity checks
        # TODO: check exception handling for AssertionError
        assert isinstance(data_in, dict), "Data payload is not a dictionary"

        # Prepare response structure
        response = self.get_envelope()

        # decode nested payload
        for real_identifier, value in data_in.items():

            # Family identifier is the first char
            identifier = real_identifier[0]

            # List continuations: If more digits follow up, decode index offset
            index_offset = 0
            try:
                index_offset = int(real_identifier[1:])
            except:  # noqa:E722
                pass

            if identifier in self.identifiers:

                rule = self.identifiers.get(identifier)
                name = rule.get("name", identifier)
                is_meta = rule.get("meta", False)

                response_key = "meta" if is_meta else "data"

                # multiple values arrive in list
                name_prefix = name
                if isinstance(value, list):
                    for idx, item in enumerate(value):
                        index = idx + 1 + index_offset
                        name = name_prefix + str(index)
                        item = self.decode_value(item, rule)
                        response[response_key][name] = item

                # single values arrive as scalar
                else:
                    value = self.decode_value(value, rule)

                    if "attname" in rule and rule["attname"] == "direct":
                        pass
                    else:
                        index = 1 + index_offset
                        name += str(index)

                    response[response_key][name] = value

        return response

    def decode_value(self, value, rule):
        if "convert" in rule:
            value = rule["convert"](value)
        if "scale-decode" in rule:
            value = rule["scale-decode"](value)
        return value

    def encode_value(self, identifier, value):
        rule = self.identifiers.get(identifier, {})
        if "scale-encode" in rule:
            value = rule["scale-encode"](value)
        return value

    def encode_values(self, identifier, values):

        # sanity checks
        assert isinstance(values, (list, tuple))

        # vararg adaptation
        if isinstance(values, tuple):
            values = list(values)

        # apply encode scaling for all values
        values = [self.encode_value(identifier, value) for value in values]

        # apply compression on single scalar values
        if len(values) == 1:
            return values[0]

        return values
