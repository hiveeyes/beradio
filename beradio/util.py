# -*- coding: utf-8 -*-
# (c) 2014,2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import sys
import logging
import json_store
from uuid import uuid4
from appdirs import user_data_dir
from datetime import datetime
from calendar import timegm
from beradio.gibberish import generate_word

class Singleton(object):
    """
    Singleton class by Duncan Booth.
    Multiple object variables refers to the same object.
    http://www.suttoncourtenay.org.uk/duncan/accu/pythonpatterns.html
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class ConfigStoreJson(dict):

    store = None
    appname = 'DEFAULT'

    def __init__(self):
        self.app_data_dir = user_data_dir(self.appname)
        #print >>sys.stderr, "ConfigStoreJson app_data_dir:", self.app_data_dir
        if not os.path.exists(self.app_data_dir):
            os.makedirs(self.app_data_dir)
        self.config_file = os.path.join(self.app_data_dir, 'config.json')
        #print >>sys.stderr, "ConfigStoreJson config_file:", self.config_file

        self.setup()

    def setup(self):
        if not ConfigStoreJson.store:
            #print "ConfigStoreJson.__init__"
            ConfigStoreJson.store = json_store.open(self.config_file)

    def has_key(self, key):
        return ConfigStoreJson.store.has_key(key)

    def __getitem__(self, key):
        #print 'ConfigStoreJson.__getitem__'
        return ConfigStoreJson.store[key]

    def __setitem__(self, key, value):
        #print 'ConfigStoreJson.__setitem__', key, value
        ConfigStoreJson.store[key] = value
        ConfigStoreJson.store.sync()


class UUIDGenerator(object):

    def get_next_id(self):
        return uuid4()


class PersistentUniqueIdentifier(Singleton):

    config = None
    identifier = 'UNKNOWN'
    attribute = 'uuid'
    store_class = ConfigStoreJson
    id_generator = UUIDGenerator().get_next_id

    def __init__(self):
        if not self.config:
            self.config = self.store_class()
        if not self.config.has_key(self.attribute) or not self.config[self.attribute]:
            self.config[self.attribute] = str(self.id_generator())
        self.identifier = self.config[self.attribute]
        #print >>sys.stderr, self.attribute + ':', self.identifier

    def __str__(self):
        return str(self.identifier)


def human_unique_id(*args):
    """
    Produces random, pronounceable pseudo-words combined with the current second.
    Examples: swan4, zech55, tug22, drew1

    .. seealso::

        https://github.com/greghaskins/gibberish
        http://www.anotherchris.net/csharp/friendly-unique-id-generation-part-2/#time
    """
    now = datetime.now()
    word = generate_word()
    unique = str(word) + str(now.second)
    return unique

def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s [%(name)-20s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=level)

def timestamp_nanos():
    """
    https://influxdb.com/docs/v0.9/troubleshooting/frequently_encountered_issues.html#querying-outside-the-min-max-time-range

        Smallest valid timestamp: -9023372036854775808 (approximately 1684-01-22T14:50:02Z)
        Largest valid timestamp: 9023372036854775807 (approximately 2255-12-09T23:13:56Z)
    """
    timestamp = datetime.utcnow()
    # from influxdb.line_protocol._convert_timestamp
    nanos = int(timegm(timestamp.utctimetuple()) * 1e9 + timestamp.microsecond * 1e3)
    return nanos

