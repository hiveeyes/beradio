# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import json
import bencode
from docopt import docopt, DocoptExit
from beradio.config import BERadioConfig
from beradio.forward import SerialToMQTT
from beradio.publish import DataToMQTT
from beradio.protocol import BERadioProtocolBase
from beradio.subscribe import MQTTSubscriber
from beradio.network import NetworkIdentifier, GatewayIdentifier, protocol_factory
from version import __VERSION__

APP_NAME = 'beradio ' + __VERSION__

def beradio_cmd():
    """
    Usage:
      beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://localhost [--protocol=<version>] [--debug]
      beradio decode <payload> [--protocol=<version>] [--debug]
      beradio info
      beradio --version
      beradio (-h | --help)

    Options:
      --source=<source>         Data source, e.g. serial:///dev/ttyUSB0
      --target=<target>         Data sink, e.g. mqtt://localhost
      --protocol=<version>      Protocol version: 1 or 2        [default: 2]
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen

    """
    options = docopt(beradio_cmd.__doc__, version=APP_NAME)
    #print 'options: {}'.format(options)

    source = options.get('--source')
    target = options.get('--target')
    protocol = options.get('--protocol')

    if options.get('forward'):
        if source.startswith('serial://') and target.startswith('mqtt://'):
            source = source.replace('serial://', '')
            target = target.replace('mqtt://', '')
            SerialToMQTT(serial_device=source, mqtt_broker=target, protocol=protocol).setup().forward()

        elif source.startswith('data://') and target.startswith('mqtt://'):
            source = source.replace('data://', '')
            target = target.replace('mqtt://', '')
            DataToMQTT(mqtt_broker=target, protocol=protocol).setup().publish(source)


        else:
            raise DocoptExit('Unable to handle combination of {} and {} in forwarding mode'.format(options.get('--source'), options.get('--target')))

    elif options.get('decode'):
        p = protocol_factory(protocol)
        payload = options.get('<payload>')
        return json.dumps(p.decode_safe(payload), indent=4)

    elif options.get('info'):
        network_id = str(NetworkIdentifier())
        gateway_id = str(GatewayIdentifier())

        print >>sys.stderr, '-' * 50
        print >>sys.stderr, APP_NAME.center(50)
        print >>sys.stderr, '-' * 50
        print >>sys.stderr, 'config file: {}'.format(BERadioConfig().config_file)
        print >>sys.stderr, 'network_id:  {}'.format(network_id)
        print >>sys.stderr, 'gateway_id:  {}'.format(gateway_id)


def bdecode_cmd():
    """
    Synopsis::

        bdecode li999ei99ei1ei2218ei2318ei2462ei2250ee
        [999, 99, 1, 2218, 2318, 2462, 2250]

        bdecode d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee
        {'h': [890, 377], 't': [3455, 3455, 3455, 3455], 'w': 12333}

    """
    if len(sys.argv) == 2:
        payload = sys.argv[1].strip()
    else:
        print >>sys.stderr, 'ERROR: Bencode data as single argument not found'
        sys.exit(1)

    # decode from Bencode format
    try:
        return BERadioProtocolBase.decode_ether(payload)

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

    if len(sys.argv) >= 2:
        return bencode.bencode(sys.argv[1])

    data_01 = [999, 99, 1, 2218, 2318, 2462, 2250]
    data_02 = {
        't': [1234, 5678, 4242],
        'h': [587, 476],
        'w': 42
    }
    data_03 = {'#': 2, '_': 'h1', 't': [2163, 1925, 1092, 1354], 'h': [488, 572], 'w': 10677}
    return bencode.bencode(data_03)


def bemqtt_cmd():
    """
    Usage:
      bemqtt subscribe [<topic>] --source=mqtt://localhost [--debug]
      bemqtt --version
      bemqtt (-h | --help)

    Options:
      --source=<source>         Data source, e.g. mqtt://localhost
      --version                 Show version information
      --debug                   Enable debug messages
      -h --help                 Show this screen

    """

    options = docopt(bemqtt_cmd.__doc__, version=APP_NAME)
    #print 'options: {}'.format(options)

    source = options.get('--source')
    if options.get('subscribe'):
        topic = options.get('<topic>')

        if source.startswith('mqtt://'):
            source = source.replace('mqtt://', '')
            MQTTSubscriber(mqtt_broker=source).setup().subscribe(topic)
