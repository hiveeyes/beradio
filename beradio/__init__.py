# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import sys
import bencode
from beradio.protocol import BERadioProtocolBase


def cmd_bedecode():
    """
    Synopsis::

        bedecode li999ei99ei1ei2218ei2318ei2462ei2250ee
        [999, 99, 1, 2218, 2318, 2462, 2250]

        bedecode d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee
        {'h': [890, 377], 't': [3455, 3455, 3455, 3455], 'w': 12333}

    """
    if len(sys.argv) == 2:
        payload = sys.argv[1].strip()
    else:
        print >>sys.stderr, 'ERROR: Bencode data as single argument not found'
        sys.exit(1)

    # decode from Bencode format
    try:
        return BERadioProtocolBase.decode(payload)

    except ValueError:
        sys.exit(1)


def cmd_beencode():
    """
    Synopsis::

        beencode [999, 99, 1, 2218, 2318, 2462, 2250]
        li999ei99ei1ei2218ei2318ei2462ei2250ee

        beencode {'h': [890, 377], 't': [3455, 3455, 3455, 3455], 'w': 12333}
        d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee

    """
    data_01 = [999, 99, 1, 2218, 2318, 2462, 2250]
    data_02 = {
        't': [1234, 5678, 4242],
        'h': [587, 476],
        'w': 42
    }
    return bencode.bencode(data_01)


def cmd_beradio_encode():
    pass

def cmd_beradio_decode():
    pass
