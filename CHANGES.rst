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
- improve JSON-over-MQTT format


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
