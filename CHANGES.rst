.. beradio-changes:

#######
CHANGES
#######


unreleased
==========


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
