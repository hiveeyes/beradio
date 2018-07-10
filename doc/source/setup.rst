
.. _beradio-setup:

#####
Setup
#####


**************
Python package
**************

Install most recent *BERadio* Python package from PyPI::

    pip install beradio --upgrade


Install a specific *BERadio* release::

    pip install beradio==0.8.1


For a quick check if everything is in place, try::

    beradio info

This should emit something like::

    --------------------------------------------------
                      beradio 0.8.1
    --------------------------------------------------
    config file: /Users/amo/Library/Application Support/beradio/config.json
    network_id:  696e4192-707f-4e8e-9246-78f6b41a280f
    gateway_id:  tug22



***************
Getting started
***************
For further details, please visit the :ref:`handbook`.


******************
Running as service
******************
For running BERadio as a system service, you might want to use one of the
prepared init system scripts as a blueprint. Please make sure you edit all
the important details to match your environment.

You will find appropriate installation instructions inside each file.

- For Debian-based systems, there's a systemd unit file, `beradio.service`_
- For OpenWrt/LEDE systems, there's an old-style init script, `beradio.init`_

.. _beradio.service: https://github.com/hiveeyes/beradio/blob/master/packaging/systemd/beradio.service
.. _beradio.init: https://github.com/hiveeyes/beradio/blob/master/packaging/openwrt/beradio.init



*******************
Development sandbox
*******************
For installing *BERadio* in development mode, see :ref:`hacking`.


----

Have fun!
