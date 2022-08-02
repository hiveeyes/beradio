# -*- coding: utf-8 -*-
# (c) 2011 Eran Sandler <eran@sandler.co.il>
# (c) 2012 David Koblas
# (c) 2014 Học Đỗ <hoc3010@gmail.com>
# (c) 2015 Andreas Motl <andreas@hiveeyes.org>
# https://github.com/erans/pysnowflake
# https://github.com/koblas/pysnowflake
# https://github.com/tarzanjw/pysnowflake
# https://github.com/tarzanjw/pysnowflake/blob/master/snowflake/server/generator.py
import logging
import time

EPOCH_TIMESTAMP = 550281600000


class SnowflakeGenerator(object):
    def __init__(self, datacenter_id, worker_id):
        self.dc = datacenter_id
        self.worker = worker_id
        self.node_id = ((self.dc & 0x03) << 8) | (self.worker & 0xFF)
        self.last_timestamp = EPOCH_TIMESTAMP
        self.sequence = 0
        self.sequence_overload = 0
        self.errors = 0
        self.generated_ids = 0

    def get_next_id(self):
        curr_time = int(time.time() * 1000)

        if curr_time < self.last_timestamp:
            # stop handling requests til we've caught back up
            self.errors += 1
            raise AssertionError("Clock went backwards! %d < %d" % (curr_time, self.last_timestamp))

        if curr_time > self.last_timestamp:
            self.sequence = 0
            self.last_timestamp = curr_time

        self.sequence += 1

        if self.sequence > 4095:
            # the sequence is overload, just wait to next sequence
            logging.warning("The sequence has been overload")
            self.sequence_overload += 1
            time.sleep(0.001)
            return self.get_next_id()

        generated_id = ((curr_time - EPOCH_TIMESTAMP) << 22) | (self.node_id << 12) | self.sequence

        self.generated_ids += 1
        return generated_id

    @property
    def stats(self):
        return {
            "dc": self.dc,
            "worker": self.worker,
            "timestamp": int(time.time() * 1000),  # current timestamp for this worker
            "last_timestamp": self.last_timestamp,  # the last timestamp that generated ID on
            "sequence": self.sequence,  # the sequence number for last timestamp
            "sequence_overload": self.sequence_overload,  # the number of times that the sequence is overflow
            "errors": self.errors,  # the number of times that clock went backward
        }
