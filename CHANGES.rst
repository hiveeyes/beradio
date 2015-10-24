===============
BERadio CHANGES
===============


develop
-------
- improve documentation, cleanups
- nail name to “BERadio”
- reflect "BERadio" in class naming, make beradio-1.0 work again
- large refactoring, many improvements
- central entrypoint script ``beradio``
- implement beradio-2.0


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
