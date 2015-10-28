.. _tasks:

=====
Tasks
=====

Prio 1
------
- [x] properly finish beradio-2 convenience in forwarding and manipulation code
- [x] don't pretend on nodeid=2, neither use it for documentation, use nodeid=999 instead!
- [x] release management
- [x] add software tests
- [o] move some stuff out of README.rst, place into network.rst and also publish @ kotori-daq
- [o] start with libberadio c++
- [o] improve inline docs

Prio 2
------
- properly handle profile => ruleset dispatching
- care about proper addressing: e.g. take address information completely out of the message, but use identifier from gateway instead!?
- refactor out topic computation from MQTTPublisher.publish_point

Prio 3
------
- TODO: What about other bus systems, like WAMP? See also https://github.com/goeddea/scratchbox/blob/master/yun/serial_to_wamp.js
