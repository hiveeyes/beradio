
.. _beradio-setup:

#####
Setup
#####

For installing *BERadio* in development mode, see :ref:`hacking`.

******
Python
******

Python package
==============

Stable release
--------------
Install most recent *BERadio* Python distribution::

    pip install --extra-index-url=https://packages.hiveeyes.org/hiveeyes/python/eggs/ beradio [--upgrade]

.. note::

    Use the ``--upgrade`` option when upgrading from an already installed package.

Specific release
----------------
Install *BERadio* version 0.8.1::

    pip install --extra-index-url=https://packages.hiveeyes.org/hiveeyes/python/eggs/ beradio==0.8.1

.. tip::

    See also :ref:`pypi-register` for registering your local pip
    with the package repository on packages.hiveeyes.org.

Uninstall
---------
::

    pip uninstall beradio --yes


Running
=======

See :ref:`handbook`.

For a quick check if everything is in place, try::

    beradio info

This should emit something like::

    --------------------------------------------------
                      beradio 0.8.1
    --------------------------------------------------
    config file: /Users/amo/Library/Application Support/beradio/config.json
    network_id:  696e4192-707f-4e8e-9246-78f6b41a280f
    gateway_id:  tug22


********
Appendix
********

.. _pypi-register:

Add PyPI repository
===================
The most convenient way would be to add the package repository
as an ``extra-index-url`` to your ``pip.conf``.

cat ~/.pip/pip.conf::

    [global]
    extra-index-url = https://packages.hiveeyes.org/hiveeyes/python/eggs/

This makes further installing and upgrading a breeze::

    pip install beradio [--upgrade]

.. note::

    Be aware when installing packages unknown to PyPI, there will be additional requests issued to
    the repository in ``extra-index-url``, which can cause further delays on failing attempts like::

        pip install Hotzenplotz

    On the other hand, each time installing a custom package, PyPI is requested first, so your actions
    **will** hit https://pypi.python.org/pypi/Hotzenplotz . Again, please be aware of that.


Troubleshooting
===============

Reading from serial line
------------------------
::

    pip install ino
    ino serial -b 115200
