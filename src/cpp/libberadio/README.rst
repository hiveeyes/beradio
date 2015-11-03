======================
libberadio c++ library
======================


Packet size and fragmentation
=============================

The maximum payload length is defined in `RFM69.h#L35`_::

    // to take advantage of the built in AES/CRC we want to limit the frame size
    // to the internal FIFO size (66 bytes - 3 bytes overhead - 2 bytes crc)
    #define RF69_MAX_DATA_LEN       61


.. _RFM69.h#L35: https://github.com/LowPowerLab/RFM69/blob/master/RFM69.h#L35
