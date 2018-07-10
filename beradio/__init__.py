# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <richard@hiveeyes.org>
# (c) 2015 Andreas Motl <andreas@hiveeyes.org>
"""BERadio spec and reference implementation"""
__version__ = '0.11.0'


def program_name(with_version=False):
    name = u'beradio'
    if with_version:
        name += u' ' + __version__
    return name
