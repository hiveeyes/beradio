#######
CHANGES
#######


in progress
===========


2018-07-11 0.12.0
=================
- Add old-style init script for OpenWrt/LEDE
- Upgrade to ``paho-mqtt==1.3.1``
- Improve logging
- Increase publishing interval for "func:sine" to 0.5 seconds
- Improve MQTT broker connection handling and logging
- Publish block message to "data.json" suffix before publishing discrete values
- After connecting, publish "alive" message to MQTT bus
- Compute appropriate "client_id" before connecting
- Disable publishing all measurements as discrete values for the time being
- Adapt MQTT topic to new-style discrete-value convention:
  Use ``/data/{fieldname}`` instead of ``/measure/{fieldname}``
- Add ``--log`` command line parameter to control log target
- Don't hardcode realm / topic prefix, get rid of specifics like ``beradio`` or ``hiveeyes`` there
- Heartbeat mechanism: Publish status information to ``status.json`` each 5 minutes
- Heartbeat mechanism: Publish status information before shutdown
- Clean ups, naming things, tests


2017-07-15 0.11.0
=================
- Also accept payload data from STDIN for JobeeMonitor environment


2017-07-15 0.10.0
=================
- Tweaks for operating on a LinkIt Smart 7688 Duo
- Add daemonization scripts for systemd and procd
- Remove “hello world” message on startup
- Update documentation
- Add decoder for JobeeMonitor UART line format


2017-04-03 0.9.0
================
- Update MQTT topic suffix ``message-json`` to ``data.json``
- Enable specifying MQTT authentication credentials from the command line


2017-04-02 0.8.1
================

- Mitigate some problems when installing on `LinkIt Smart 7688 Duo`_:

    - Fix setup documentation re. ``--extra-index-url``, see also
      `Problems installing BERadio on OpenWrt/LEDE with "--index-url" <https://community.hiveeyes.org/t/problems-installing-beradio-on-openwrt-lede/228/3>`_.
    - Fix “appdir” module dependency woes, see also
      `Problems installing BERadio on OpenWrt/LEDE with "appdirs" module <https://community.hiveeyes.org/t/problems-installing-beradio-on-openwrt-lede/228/7>`_.

Thanks, Richard and Martin!


2016-09-30 0.8.0
================
- Add ad hoc CSV payload decoding for making things work with Open Hive firmwares


.. _BERadio 0.7.0:

2016-07-10 0.7.0
================
- Move from mosquitto library to paho-mqtt


.. _BERadio 0.6.0:

2016-07-10 0.6.0
================
- Revert scaling factors, Update tests
- List continuations: If digits follow after family identifiers, decode index offset
- Add “rssi” family identifier (again) and “loop” (new)


.. _BERadio 0.5.0:

2016-03-07 0.5.0
================

``beradio-python``
------------------
- Add :any:`BERadioMessage` as a convenient message builder, with api docs and doctests
- Improve mqtt broker reconnect behavior
- Add nanosecond timestamp to json mqtt message
- Use shorter unique id as gateway id
- Improve commandline publisher: single measurements, multiple measurements,
  some math functions (triangle, square, sawtooth, sine)

- Add some lines about how to :ref:`bemqtt` using the new command ``bemqtt``
- Add document :ref:`serialization-size-comparison` as a shootout between
  BERadio vs. Bencode vs. Binary vs. CSV vs. JSON vs. YAML
- Wording: rename “topic_domain” to “realm”

- Add software testing framework "nose"
- Add some doctests for ``protocol.py``
- Improve logging
- Refactor Makefile targets re. mqtt publishing
- Improve convenient releasing and installing

``libberadio``
--------------
- add c++ spike using variadic arguments and stl vectors based on avr-stl, works in SimulAVR
- add varargs.h, improve variadic argument reading
- improve vararg handling, introduce more convenient data type name aliases
  "FloatList" and "IntegerList", make "dump_vector" work generic
- add simple message encoding on top of Bencode
- switch from avr-stl to StandardCplusplus, which runs out-of-the-box and even produces smaller binaries
- use "-mcall-prologues" for producing smaller binaries (~400 bytes)

common
------
- Improve documentation significantly


.. _BERadio 0.4.4:

2015-10-27 0.4.4
================
- fully automatic package building and publishing
- releases 0.4.2 and 0.4.3 were spent on getting things right


2015-10-27 0.4.1
================
- improve automatic release management


2015-10-27 0.4.0
================
- nail name to “BERadio”
- reflect "BERadio" in class naming, make beradio-1.0 work again
- large refactoring, many improvements
- central entrypoint scripts ``beradio`` and ``bdecode``
- implement BERadio specification version 2
- add Sphinx document generator
- add ``bemqtt``, a basic but convenient MQTT subscriber for debugging purposes
- in the intermediary message format, all identifiers (network, gateway, node) are strings
- add unique identifier generation based on uuid4 and Snowflake, see also ``beradio info``
- don't pretend on nodeid=2, neither use it for documentation, use nodeid=999 instead


2015-10-19 0.0.3
================
- improve documentation, cleanups


2015-10-18 0.0.2
================
- production improvements
- be more graceful when receiving invalid Bencode payloads
- fix mqtt publisher in forwardings scenario
- properly sanitize serial input data
- pretending dry-run publisher using random data


2015-10-17 0.0.1
================
- initial commit of "serial-to-mqtt" proof-of-concept prototype
