.. include:: links.rst

##############
BERadio README
##############

.. tip::

    You might want to `read this document on our documentation space <https://hiveeyes.org/docs/beradio/README.html>`_,
    all inline links will be working there.


*BERadio* is an encoding specification and implementation for efficient communication in
constrained radio link environments.
It is conceived and used for over-the-air communication within the `Hiveeyes project`_.

Together with :ref:`Kotori`, a multi-channel, multi-protocol data acquisition and graphing toolkit
for building flexible telemetry solutions, it powers the `Hiveeyes system`_
on the gateway side, which you can enjoy by visiting the `Hiveeyes platform`_.

Feel welcome to join us!

.. note::

    For setup information, go straight to the :ref:`beradio-setup` documentation.
    To get an idea about the feature set, take a glimpse into the :ref:`handbook`.
    If you want to modify the source to adapt to your needs,
    you might want to look at :ref:`hacking`.


Intro
=====
There are a number of Arduino sensor nodes in the field communicating unidirectionally
via radio link to a central Arduino acting as a gateway. The gateway Arduino receives
message payloads and writes them verbatim to the serial port connected to a Raspberry Pi,
which transforms and forwards the messages to a MQTT bus.

The data now being on the bus, arbitrary systems can consume information by subscribing
to specific MQTT topics where measurement events are delivered.

The Kotori multichannel DAQ subscribes to topics on the MQTT bus, receives telemetry data
payloads and stores the measurements into a contemporary timeseries database.
After that, Grafana is used to display the measurement information.


About
=====
*BERadio* is a specification and also provides reference implementations for Arduino and Python.

- It uses the ``Bencode`` format on the wire to provide space-efficient data encoding.
- ``beradio forward`` processes data messages received over the air and forwards them to MQTT.
- ``libberadio`` will be an appropriate C++ library for Arduino.


Specification
-------------
.. toctree::
    :maxdepth: 2

    beradio


Implementation
--------------
``beradio forward`` ingests message payloads from a serial interface, sanitizes and
decodes them from ``Bencode`` format and republishes the data to a MQTT topic.

The MQTT topic name is derived from some parameters contained in the data
of the message, the topic template used for this is currently programmed
to ``{realm}/{network}/{gateway}/{node}/{field}``, where ``realm=hiveeyes``.
The actual values will get separated, mapped and formatted in different
variants before republishing them to MQTT.


Architecture
============
We are standing on the shoulders of giants.
Read about the technologies, standards, protocols and subsystems
used for building the whole system at :ref:`hiveeyes-foundation`.

Read more about the :ref:`hiveeyes-one-architecture` and different
scenarios the components are used in, like :ref:`hiveeyes-one-swarm-setup`
and :ref:`hiveeyes-one-island-setup`.


Credits
=======
- computourist_ for the `RFM69 based sensors and MQTT gateway`_
  giving us a rough idea where to move.
- `Felix Rusu`_ of LowPowerLab_ fame for conceiving the fine `RFM69 library`_.
- `Jean-Claude Wippler`_ of JeeLabs_ fame for building the `JeeLink v3c`_ (`shop <JeeLink v3c shop>`_),
  a fully assembled and ready-to-use USB "stick" containing an Atmel ATmega328p AVR microprocessor
  and a HopeRF RFM69CW wireless radio module. Also for conceiving the fine EmBencode_ C++ library.
- Weef for suggesting the Bencode_ format.
- Franky for spending two whole afternoons at *Chaos Communication Camp 2015* for
  hunting down and fixing the `EmBencode encoding bug`_ on Arduino_.
- `A Python script to push serial data to MQTT`_
  for getting us started on the MQTT_ side.
  Based on work from `Andy Piper`_ (2011) and `Didier Donsez`_ (2014).
