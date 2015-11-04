======================
libberadio c++ library
======================

Dependencies
============

avr-stl
-------
| The Standard Template Library (STL) for AVR with C++ streams
| Version 1.1.1 (most recent as of 2015-11-01)
| http://andybrown.me.uk/2011/01/15/the-standard-template-library-stl-for-avr-with-c-streams/
| https://drive.google.com/uc?export=download&id=0B9Zobp2aWUKzb2xvZ0Y2VGd1RTQ

Packet size and fragmentation
=============================

The maximum payload length is defined in `RFM69.h#L35`_::

    // to take advantage of the built in AES/CRC we want to limit the frame size
    // to the internal FIFO size (66 bytes - 3 bytes overhead - 2 bytes crc)
    #define RF69_MAX_DATA_LEN       61


.. _RFM69.h#L35: https://github.com/LowPowerLab/RFM69/blob/master/RFM69.h#L35
