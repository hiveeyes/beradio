# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from beradio import __appname__
from beradio.util import ConfigStoreJson

class BERadioConfig(ConfigStoreJson):
    appname = __appname__
