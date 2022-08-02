# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl <andreas@hiveeyes.org>
from beradio import __appname__
from beradio.util import ConfigStoreJson


class BERadioConfig(ConfigStoreJson):
    appname = __appname__
