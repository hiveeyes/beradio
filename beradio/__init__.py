# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <richard@hiveeyes.org>
# (c) 2015 Andreas Motl <andreas@hiveeyes.org>
"""BERadio spec and reference implementation"""
__appname__ = "beradio"
__version__ = "0.13.0"


def program_name(with_version=False):
    name = __appname__
    if with_version:
        name += " " + __version__
    return name
