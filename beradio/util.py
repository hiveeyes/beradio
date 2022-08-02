# -*- coding: utf-8 -*-
# (c) 2014-2022 Andreas Motl <andreas@hiveeyes.org>
import logging
import os
import socket
import sys
import traceback
from calendar import timegm
from datetime import datetime
from io import StringIO
from math import sin
from uuid import uuid4

import json_store
from appdirs import user_data_dir

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
    appname = "DEFAULT"

    def __init__(self):
        self.app_data_dir = user_data_dir(self.appname)
        # print("ConfigStoreJson app_data_dir:", self.app_data_dir, file=sys.stderr)
        if not os.path.exists(self.app_data_dir):
            os.makedirs(self.app_data_dir)
        self.config_file = os.path.join(self.app_data_dir, "config.json")
        # print("ConfigStoreJson config_file:", self.config_file, file=sys.stderr)

        self.setup()

    def setup(self):
        if not ConfigStoreJson.store:
            # print("ConfigStoreJson.__init__", file=sys.stderr)
            ConfigStoreJson.store = json_store.open(self.config_file)

    def has_key(self, key):
        return key in ConfigStoreJson.store

    def __getitem__(self, key):
        # print('ConfigStoreJson.__getitem__', file=sys.stderr)
        return ConfigStoreJson.store[key]

    def __setitem__(self, key, value):
        # print('ConfigStoreJson.__setitem__', key, value, file=sys.stderr)
        ConfigStoreJson.store[key] = value
        ConfigStoreJson.store.sync()


class UUIDGenerator(object):
    def get_next_id(self):
        return uuid4()


class PersistentUniqueIdentifier(Singleton):

    config = None
    identifier = "UNKNOWN"
    attribute = "uuid"
    store_class = ConfigStoreJson
    id_generator = UUIDGenerator().get_next_id

    def __init__(self):
        if not self.config:
            self.config = self.store_class()
        if self.attribute not in self.config or self.config[self.attribute] is None:
            self.config[self.attribute] = str(self.id_generator())
        self.identifier = self.config[self.attribute]
        # print(self.attribute + ':', self.identifier, file=sys.stderr)

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


def setup_logging(output="-", level=logging.INFO):
    log_format = "%(asctime)-15s [%(name)-20s] %(levelname)-7s: %(message)s"

    if output == "-":
        logging.basicConfig(stream=sys.stderr, format=log_format, level=level)

    else:
        logging.basicConfig(filename=output, format=log_format, level=level)


def timestamp_nanos():
    """
    https://docs.influxdata.com/influxdb/v0.13/troubleshooting/frequently_encountered_issues/#querying-outside-the-min-max-time-range

        Smallest valid timestamp: -9023372036854775808 (approximately 1684-01-22T14:50:02Z)
        Largest valid timestamp: 9023372036854775807 (approximately 2255-12-09T23:13:56Z)
    """
    timestamp = datetime.utcnow()
    # from influxdb.line_protocol._convert_timestamp
    nanos = int(timegm(timestamp.utctimetuple()) * 1e9 + timestamp.microsecond * 1e3)
    return nanos


def math_func(name, x, amplitude=10):
    """
    https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave

    .. see also::

        - https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.sawtooth.html
        - https://gist.github.com/endolith/407991
        - https://code.activestate.com/recipes/577592-simple-1khz-audio-function-generator-using-standar/
    """
    x = float(x)
    y = x

    # triangle
    if name == "triangle":
        y = abs((x % (amplitude * 2)) - amplitude)
        # y = amplitude - abs(x % (2*amplitude) - amplitude)

    # square
    elif name == "square":
        y = (x % (amplitude * 2)) < amplitude and amplitude or 0

    # sawtooth
    elif name == "sawtooth":
        y = round((x / amplitude - int(x / amplitude)) * amplitude)

    # sine
    elif name == "sine":
        y = amplitude * sin(x / 10)

    else:
        raise NotImplementedError('Math func "{}" not implemented'.format(name))

    return y


def traceback_get_exception(num=-1):

    # build error message
    exception_string = "".join(
        traceback.format_exception_only(sys.exc_type, hasattr(sys, "exc_value") and sys.exc_value or "Unknown")
    )

    # extract error location from traceback
    if hasattr(sys, "exc_traceback"):
        (filename, line_number, function_name, text) = traceback.extract_tb(sys.exc_traceback)[num]
    else:
        (filename, line_number, function_name, text) = ("-", "-", "-", "-")

    error = {
        "message": exception_string,
        "location": {
            "filename": filename,
            "line_number": line_number,
            "function_name": function_name,
            "text": text,
        },
    }

    return error


def format_exception_location(error, prefix=""):
    if prefix:
        prefix += "\n"
    error_location = prefix + "Filename:    %s\nLine number: %s\nFunction:    %s\nCode:        %s" % (
        error["location"]["filename"],
        error["location"]["line_number"],
        error["location"]["function_name"],
        error["location"]["text"],
    )
    return error_location


def last_error_and_traceback():
    error_entry = traceback_get_exception(0)
    error_last = traceback_get_exception(-1)
    sep = "-" * 60
    payload_location = "\n".join(
        [
            sep,
            format_exception_location(error_entry, "Entry point:"),
            sep,
            format_exception_location(error_last, "Source of exception:"),
        ]
    )
    payload = "".join(["ERROR: ", error_entry["message"], "\n", payload_location, "\n"])

    # add full traceback
    buffer = StringIO()
    traceback.print_exc(file=buffer)
    buffer.seek(0)
    payload += "\n" + buffer.read()

    return payload


def get_hostname():
    return socket.gethostname()
