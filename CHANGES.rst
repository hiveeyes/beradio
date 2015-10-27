Changes in BERadio
==================


develop
-------
- improve documentation, cleanups
- nail name to “BERadio”
- reflect "BERadio" in class naming, make beradio-1.0 work again
- large refactoring, many improvements
- central entrypoint scripts ``beradio`` and ``bedecode``
- implement BERadio specification version 2
- add Sphinx document generator
- add ``bemqtt``, a basic but convenient MQTT subscriber for debugging purposes
- in the intermediary message format, all identifiers (network, gateway, node) are strings
- default network identifier is ``test``
- add unique identifier generation based on uuid4 and Snowflake, see also ``beradio info``

2015-10-18 0.0.2
----------------
- production improvements
- be more graceful when receiving invalid Bencode payloads
- fix mqtt publisher in forwardings scenario
- properly sanitize serial input data
- pretending dry-run publisher using random data


2015-10-17 0.0.1
----------------
- initial commit of "serial-to-mqtt" proof-of-concept prototype
