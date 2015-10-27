.. _setup:

=====
Setup
=====

Interested in installing *BERadio* in development mode? See :ref:`hacking`.

Ad hoc
------

Install most recent ``beradio`` Python distribution::

    pip install --index-url=https://packages.elmyra.de/hiveeyes/python/eggs/ beradio [--upgrade]

.. note::

    Use the ``--upgrade`` option when upgrading from an already installed package.

Install specific release::

    pip install https://packages.elmyra.de/hiveeyes/python/eggs/beradio-0.4.4.tar.gz
    pip install --index-url=https://packages.elmyra.de/hiveeyes/python/eggs/ beradio==0.4.4


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


Troubleshooting
===============

Reading from serial line
------------------------
::

    pip install ino
    ino serial -b 115200
