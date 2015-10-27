# -*- coding: utf-8 -*-
# (c) 2014,2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from posix import getpid
from beradio.config import BERadioConfig
from beradio.protocol import BERadioProtocol1, BERadioProtocol2
from beradio.snowflake import SnowflakeGenerator
from beradio.util import PersistentUniqueIdentifier

class NetworkIdentifier(PersistentUniqueIdentifier):
    store_class = BERadioConfig
    attribute = 'network_id'

class GatewayIdentifier(PersistentUniqueIdentifier):
    store_class = BERadioConfig
    attribute = 'gateway_id'
    datacenter = 0
    id_generator = SnowflakeGenerator(datacenter, getpid()).get_next_id

def protocol_factory(version):

    network_id = str(NetworkIdentifier())
    gateway_id = str(GatewayIdentifier())

    version = str(version)
    if version == '1':
        class_ = BERadioProtocol1
    elif version == '2':
        class_ = BERadioProtocol2
    else:
        class_ = BERadioProtocol2

    return class_(network_id=network_id, gateway_id=gateway_id)