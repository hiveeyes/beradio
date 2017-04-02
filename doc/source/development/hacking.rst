.. _hacking:

==================
Hacking on BERadio
==================


Code repository
===============

*BERadio* is hosted at:

    https://github.com/hiveeyes/beradio


Getting the code
----------------
::

    git clone https://github.com/hiveeyes/beradio
    cd beradio


Installation
============
- Prepare Python environment::

    aptitude install python-virtualenv
    virtualenv --no-site-packages .venv27
    source .venv27/bin/activate

    # install dependencies and entrypoints
    python setup.py develop


Running the tests
=================
This describes running tests, checking code coverage and a bit of how to actually write tests using ``doctest``.
::

    make test

Display detailed test coverage::

    make test-coverage
    open coverage/html/index.html

For writing doctests, please have a look at the fine documentation:
- https://docs.python.org/2/library/doctest.html
- https://pymotw.com/2/doctest/



Running the program
===================

Quickstart
----------

Publish multiple measurements::

    make publish-docker data='json:{"temperature": 42.84, "humidity": 83}'

Publish single measurement::

    make publish-docker data='value:{"volume": 72}'

Publish waveform data to MQTT broker running inside a Docker container::

    make publish-docker-func func=sine

.. seealso:: :ref:`handbook`


Cutting a release and package publishing
========================================
To build a ``sdist`` Python package and upload it to the designated package repository,
just run for regular ``minor`` releases::

    make release bump=minor

If it is really just a bugfix, cut a ``patch`` release::

    make release bump=patch

If things went far, a ``major`` release might be indicated::

    make release bump=major


Deployment
==========
It is currently hot-deployed to ``~/hiveeyes/beradio`` on *einsiedlerkrebs.ddns.net* using *git* and
usually running on the *master* branch inside a *tmux* session called ``BERadio``.
Feel welcome to hack away on it in this place. You can get access to our shared ``ha-devs`` environment
by sharing your ssh public keys with us.


MQTT topic computing
====================

The second most common thing to amend is probably the way how topic names are computed.

Find its definition in ``beradio/mqtt.py`` lines 116 ff.::

    class BERadioMQTTPublisher(MQTTPublisher):
        topic_template = u'{realm}/{network}/{gateway}/{node}/{name}'

Regarding topic naming, please have a look at :ref:`mqtt-resources`.
