.. _setup:

=====
Setup
=====

For installing *BERadio* in development mode, see :ref:`hacking`.

Ad hoc
------

Install most recent *BERadio* Python distribution::

    pip install --index-url=https://packages.elmyra.de/hiveeyes/python/eggs/ beradio [--upgrade]

.. note::

    Use the ``--upgrade`` option when upgrading from an already installed package.

Install specific release::

    pip install --index-url=https://packages.elmyra.de/hiveeyes/python/eggs/ beradio==0.4.4
    pip install https://packages.elmyra.de/hiveeyes/python/eggs/beradio-0.4.4.tar.gz


Add package repository as an ``extra-index-url``
------------------------------------------------
The most convenient way.

cat ~/.pip/pip.conf::

    [global]
    extra-index-url = https://packages.elmyra.de/hiveeyes/python/eggs/

This makes further installing and upgrading a breeze::

    pip install beradio [--upgrade]


.. note::

    Be aware when installing packages unknown to PyPI, there will be additional requests issued to
    the repository in ``extra-index-url``, which can cause further delays on failing attempts like::

        pip install Hotzenplotz

    On the other hand, each time installing a custom package, PyPI is requested first, so your actions
    **will** hit https://pypi.python.org/pypi/Hotzenplotz . Again, please be aware of that.


Uninstall
---------
::

    pip uninstall beradio --yes


Running
=======

See :ref:`handbook`.

For a quick check if everything is in place, try::

    beradio info

It should emit something like::

    --------------------------------------------------
                      beradio 0.4.4
    --------------------------------------------------
    config file: /Users/amo/Library/Application Support/beradio/config.json
    network_id:  696e4192-707f-4e8e-9246-78f6b41a280f
    gateway_id:  tug22


Troubleshooting
===============

Reading from serial line
------------------------
::

    pip install ino
    ino serial -b 115200
