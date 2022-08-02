# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@hiveeyes.org>
from collections import OrderedDict


def jobee_decode(line):
    """
    Decode JobeeMonitor line format
    See also https://github.com/Jodaille/JobeeMonitor/blob/master/JobeeMonitor/JobeeMonitor.ino

    Example::

        id=Danvou;lux=13940.88;bmpP=997.03;bmpT=20.32;topT=0;entryT=0;h=70.55;siT=19.38;rainLevel=2.24;RainFall=466;milli=332143870;

    """
    data = OrderedDict()
    parts = line.split(";")
    for part in parts:
        try:
            key, value = part.split("=")
            data[key.strip()] = value.strip()
        except:  # noqa:E722
            pass
    return data


if __name__ == "__main__":
    line = (
        "id=Danvou;lux=13940.88;bmpP=997.03;bmpT=20.32;topT=0;entryT=0;"
        "h=70.55;siT=19.38;rainLevel=2.24;RainFall=466;milli=332143870;"
    )
    print(jobee_decode(line))
