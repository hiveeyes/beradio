.. _setup:

=====
Setup
=====


Installation
============
- Prepare Python environment::

    aptitude install python-virtualenv
    virtualenv --no-site-packages .venv27
    source .venv27/bin/activate

    # pyserial, mosquitto, bencode
    pip install -r requirements.txt


Running
=======
See also `<handbook.rst>`__.


Run forwarder
-------------

Publish serial data to MQTT broker running on the same machine::

    make forward


Run pretend publisher
---------------------

Publish fixed data to MQTT broker running on localhost::

    make pretend-local

Publish random data to MQTT broker running inside a Docker container::

    make pretend-docker-random



Troubleshooting
===============

Reading from serial line
------------------------
::

    pip install ino
    ino serial -b 115200
