.. include:: links.rst

.. BERadio documentation master file, created by
   sphinx-quickstart on Wed Oct 25 00:14:04 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _beradio:

#######
BERadio
#######

*****
About
*****
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

----

.. toctree::
    :caption: About
    :maxdepth: 1

    README
    beradio
    credits


.. toctree::
    :caption: Usage
    :maxdepth: 1

    setup
    handbook
    development/api
    hiveeyes


.. toctree::
    :caption: Project information
    :maxdepth: 1
    :glob:

    Changelog <changes>
    development/source
    development/backlog


.. toctree::
    :caption: Development
    :maxdepth: 1
    :glob:

    development/sandbox
    development/documentation


.. toctree::
    :caption: Software tests
    :maxdepth: 1

    test/beradio
    test/reassembly


.. toctree::
    :caption: Research
    :maxdepth: 1
    :glob:

    research/prior-art
    research/mqtt
    test/serialization-size
    research/arduino-cpp
    research/firmware-size
    research/notepad


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

