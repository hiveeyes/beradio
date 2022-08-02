# -*- coding: utf-8 -*-
# (c) 2014-2015 Andreas Motl <andreas@hiveeyes.org>
from posix import getpid

from beradio.config import BERadioConfig
from beradio.protocol import BERadioProtocol1, BERadioProtocol2
from beradio.snowflake import SnowflakeGenerator
from beradio.util import PersistentUniqueIdentifier, human_unique_id


class NetworkIdentifier(PersistentUniqueIdentifier):
    store_class = BERadioConfig
    attribute = "network_id"


class IdentifierSnowflake(PersistentUniqueIdentifier):
    store_class = BERadioConfig
    attribute = "gateway_id"
    datacenter = 0
    id_generator = SnowflakeGenerator(datacenter, getpid()).get_next_id


class IdentifierHuman(PersistentUniqueIdentifier):
    store_class = BERadioConfig
    attribute = "gateway_id"
    id_generator = human_unique_id


GatewayIdentifier = IdentifierHuman


def protocol_factory(version=None):

    network_id = str(NetworkIdentifier())
    gateway_id = str(GatewayIdentifier())

    version = str(version)
    if version == "1":
        class_ = BERadioProtocol1
    elif version == "2":
        class_ = BERadioProtocol2
    else:
        class_ = BERadioProtocol2

    return class_(network_id=network_id, gateway_id=gateway_id)
