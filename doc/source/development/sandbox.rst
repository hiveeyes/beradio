.. _sandbox:
.. _hacking:

===============
BERadio sandbox
===============


Code repository
===============

*BERadio* is hosted at:

    https://github.com/hiveeyes/beradio


Setup
=====

Get the sources and invoke the test suite::

    git clone https://github.com/hiveeyes/beradio
    cd beradio
    make test-coverage


Notes
=====

The process will automatically create a Python virtualenv
within the ``.venv`` directory.

Generate code coverage HTML report::

    coverage html
    open htmlcov/index.html

For writing doctests, please have a look at the fine documentation:

- https://docs.python.org/3/library/doctest.html
- https://pymotw.com/2/doctest/



Using Mosquitto in Docker
=========================

Start Mosquitto MQTT broker::

    docker run --rm -it --publish=1883:1883 --publish=9001:9001 --name=mosquitto \
        eclipse-mosquitto mosquitto -c /mosquitto-no-auth.conf

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
