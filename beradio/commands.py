# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <richard@hiveeyes.org>
# (c) 2015 Andreas Motl <andreas@hiveeyes.org>
import json
import logging
import sys

import bencode
from docopt import DocoptExit, docopt

from beradio import program_name
from beradio.config import BERadioConfig
from beradio.forward import SerialToMQTT
from beradio.network import GatewayIdentifier, NetworkIdentifier, protocol_factory
from beradio.protocol import BERadioProtocolBase
from beradio.publish import DataToMQTT
from beradio.subscribe import MQTTSubscriber
from beradio.util import setup_logging

APP_NAME = program_name(with_version=True)

logger = logging.getLogger(__name__)


def beradio_cmd():
    """
    Usage:
      beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://localhost [--protocol=<version>] [--log=<log>] [--debug]  # noqa:E501
      beradio decode <payload> [--protocol=<version>] [--debug]
      beradio info
      beradio --version
      beradio (-h | --help)

    Options:
      --source=<source>         Data source, e.g. serial:///dev/ttyUSB0
      --target=<target>         Data sink, e.g. mqtt://localhost
      --protocol=<version>      Protocol version: 1 or 2        [default: 2]
      --log=<log>               Where to send log output        [default: -]
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen

    """
    options = docopt(beradio_cmd.__doc__, version=APP_NAME)
    # print('options: {}'.format(options))

    source = options.get("--source")
    target = options.get("--target")
    protocol = options.get("--protocol")

    boot_logging(options)

    if options.get("forward"):
        if source.startswith("serial://") and target.startswith("mqtt://"):
            source = source.replace("serial://", "")
            SerialToMQTT(serial_device=source, mqtt_broker=target, protocol=protocol).setup().forward()

        elif source.startswith("data://") and target.startswith("mqtt://"):
            data = source.replace("data://", "")
            if data == "stdin":
                data = sys.stdin.read().strip()

            DataToMQTT(mqtt_broker=target, protocol=protocol).setup().publish(data)

        else:
            raise DocoptExit(
                "Unable to handle combination of {} and {} in forwarding mode".format(
                    options.get("--source"), options.get("--target")
                )
            )

    elif options.get("decode"):
        p = protocol_factory(protocol)
        payload = options.get("<payload>")
        return json.dumps(p.decode_safe(payload), indent=4)

    elif options.get("info"):
        network_id = str(NetworkIdentifier())
        gateway_id = str(GatewayIdentifier())

        print("-" * 50, file=sys.stderr)
        print(APP_NAME.center(50), file=sys.stderr)
        print("-" * 50, file=sys.stderr)
        print("config file: {}".format(BERadioConfig().config_file), file=sys.stderr)
        print("network_id:  {}".format(network_id), file=sys.stderr)
        print("gateway_id:  {}".format(gateway_id), file=sys.stderr)


def bdecode_cmd():
    """
    Synopsis::

        bdecode li999ei99ei1ei2218ei2318ei2462ei2250ee
        [999, 99, 1, 2218, 2318, 2462, 2250]

        bdecode d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee
        {'h': [890, 377], 't': [3455, 3455, 3455, 3455], 'w': 12333}

    """

    boot_logging()

    if len(sys.argv) == 2:
        payload = sys.argv[1].strip()
    else:
        logger.error("bdecode requires Bencode data as single argument")
        sys.exit(1)

    # decode from Bencode format
    try:
        return BERadioProtocolBase().decode_ether(payload)

    except ValueError:
        sys.exit(1)


def bencode_cmd():
    """
    Synopsis::

        beencode [999, 99, 1, 2218, 2318, 2462, 2250]
        li999ei99ei1ei2218ei2318ei2462ei2250ee

        beencode {'h': [890, 377], 't': [3455, 3455, 3455, 3455], 'w': 12333}
        d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee

    """

    boot_logging()

    if len(sys.argv) >= 2:
        return bencode.bencode(sys.argv[1])

    # data_01 = [999, 99, 1, 2218, 2318, 2462, 2250]
    # data_02 = {"t": [1234, 5678, 4242], "h": [587, 476], "w": 42}
    data_03 = {"#": 999, "_": "h1", "t": [2163, 1925, 1092, 1354], "h": [488, 572], "w": 10677}
    return bencode.bencode(data_03)


def bemqtt_cmd():
    """
    Usage:
      bemqtt subscribe --source=mqtt://localhost/this-topic [--topic=<topic>] [--debug]
      bemqtt --version
      bemqtt (-h | --help)

    Options:
      --source=<source>         Data source, e.g. mqtt://localhost
      --topic=<topic>           Additional fragment to append to topic from MQTT URL
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen

    """

    options = docopt(bemqtt_cmd.__doc__, version=APP_NAME)
    # print('options: {}'.format(options))

    boot_logging(options)

    source = options.get("--source")
    if options.get("subscribe"):
        topic = options.get("--topic")

        if source.startswith("mqtt://"):
            MQTTSubscriber(mqtt_broker=source).setup().subscribe(topic)

        else:
            raise NotImplementedError("Unable to subscribe to data source {}".format(source))


def boot_logging(options=None):
    options = options or {}
    log_level = logging.INFO
    output = "-"
    if options.get("--log"):
        output = options["--log"]
    if options.get("--debug"):
        log_level = logging.DEBUG

    setup_logging(output=output, level=log_level)
