# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <richard@hiveeyes.org>
# (c) 2015-2018 Andreas Motl <andreas@hiveeyes.org>
import json
import logging
import threading
import time
from collections import OrderedDict
from pprint import pformat

from beradio.protocol import BERadioProtocol2

logger = logging.getLogger(__name__)


class BERadioMessage(object):

    protocol_factory = BERadioProtocol2

    def __init__(self, nodeid, profile="h1"):
        """
        >>> message = BERadioMessage(999)

        >>> bytes(message)
        b'd1:#i999e1:_2:h1e'

        >>> message.temperature(21.63, 19.25, 10.92, 13.54)
        >>> bytes(message)
        b'd1:#i999e1:_2:h11:tli2163ei1925ei1092ei1354eee'

        >>> message.humidity(488.0, 572.0)
        >>> bytes(message)
        b'd1:#i999e1:_2:h11:hli48800ei57200ee1:tli2163ei1925ei1092ei1354eee'

        >>> message.weight(106.77)
        >>> bytes(message)
        b'd1:#i999e1:_2:h11:hli48800ei57200ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee'

        """
        self.nodeid = int(nodeid)
        self.profile = str(profile)
        self.payload = {}
        self.protocol = self.protocol_factory()

    def temperature(self, *args):
        self.payload["t"] = self.protocol.encode_values("t", args)

    def humidity(self, *args):
        self.payload["h"] = self.protocol.encode_values("h", args)

    def weight(self, *args):
        self.payload["w"] = self.protocol.encode_values("w", args)

    def clear(self):
        self.payload = {}

    def encode(self):
        data = {
            "#": self.nodeid,
            "_": self.profile,
        }
        data.update(self.payload)
        message = self.protocol.encode_ether(data)
        return message

    def __bytes__(self):
        return self.encode()

    def __repr__(self):
        data = {
            "#": self.nodeid,
            "_": self.profile,
        }
        data.update(self.payload)
        return pformat(data)

    @classmethod
    def decode(cls, payload):
        message = cls.protocol_factory().decode(payload)
        message["data"] = OrderedDict(message["data"])
        return message

    @classmethod
    def json(cls, payload):
        message = cls.protocol_factory().decode(payload)
        return json.dumps(message, sort_keys=True, indent=4)


class ResettableTimer:
    def __init__(self, interval, function):
        self.interval = interval
        self.function = function
        self.make_timer()

    def make_timer(self):
        self.timer = threading.Timer(self.interval, self.function)
        self.timer.start()

    def reset(self):

        if self.timer is None:
            self.make_timer()
        else:
            if not self.timer.finished.is_set():
                self.timer.cancel()

            self.make_timer()


class BERadioMessageDecoder(object):

    REASSEMBLY_TIMEOUT = 2.5

    # Collector mode: Wait until hitting REASSEMBLY_TIMEOUT, then return complete reassembled messages
    MODE_COLLECT = 1

    # Emitter mode: Emit reassembled fragments to all subscribers after hitting REASSEMBLY_TIMEOUT
    MODE_EMIT = 2

    def __init__(self, reassembly_timeout=None):
        self.reassembly_timeout = reassembly_timeout or self.REASSEMBLY_TIMEOUT
        self.mode = self.MODE_COLLECT
        self.timer = ResettableTimer(self.reassembly_timeout, self.release)
        self.ready = threading.Event()
        self.subscribers = []
        self.messages = []

    def subscribe(self, subscriber):
        self.mode = self.MODE_EMIT
        self.subscribers.append(subscriber)

    def release(self):
        logger.info("BERadioMessageDecoder.release")

        # Signal readiness
        self.ready.set()
        time.sleep(0.1)

        if self.mode == self.MODE_EMIT:
            self.emit()

    def emit(self):
        logger.info("BERadioMessageDecoder.emit")

        # Inform all subscribers
        payload = self.assemble()
        for subscriber in self.subscribers:
            subscriber(payload)

        # Clear buffer for next iteration
        self.messages = []

    def read(self, payload):
        logger.info("BERadioMessageDecoder.read")

        # Clear readiness indicator
        self.ready.clear()

        # Reset the timer
        self.timer.reset()

        # Collect the payload fragment
        self.messages.append(payload)

    def wait(self):

        if self.mode == self.MODE_EMIT:
            raise NotImplementedError(
                "The message decoder does not support waiting for complete packets when running in emitter mode"
            )

        logger.info("BERadioMessageDecoder.wait")

        # Wait for reassembly timeout
        self.ready.wait()

        return self.assemble()

    def to_json(self, strip_time=False):
        data = self.wait()
        payload = json.dumps(data, sort_keys=True, indent=4)
        return payload

    def assemble(self):

        if not self.messages:
            return

        data = OrderedDict()
        for payload in self.messages:

            message = BERadioMessage.decode(payload)
            # message['payload'] = payload

            node_id = message["meta"]["node"]

            if node_id not in data:
                data[node_id] = message
                data[node_id]["messages"] = [payload]
            else:
                data[node_id]["meta"].update(message["meta"])
                data[node_id]["data"].update(message["data"])
                data[node_id]["messages"].append(payload)

        return data


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    parts = []
    parts.append("d1:#i2e1:_2:h11:tli2168ei1393ei3356ei1468ei1700ee1:hlee")
    parts.append("d1:#i2e1:_2:h12:h0li8370ee1:wli53503600ei2590ee1:lli15100eee")
    parts.append("d1:#i3e1:_2:h11:tli2168ee2:h0li930ee1:wli4242eee")
    parts.append("d1:#i2e1:_2:h11:rli-6600eee")

    def emitter(data):
        logger.info("Emit:\n{}".format(json.dumps(data, indent=4)))

    decoder = BERadioMessageDecoder()
    # decoder.subscribe(emitter)

    decoder.read(parts[0])
    time.sleep(1.5)

    decoder.read(parts[1])
    time.sleep(1.5)

    decoder.read(parts[2])
    decoder.read(parts[3])

    data = decoder.wait()
    logger.info("Data:\n{}".format(json.dumps(data, indent=4)))
