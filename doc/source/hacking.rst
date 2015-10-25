.. _hacking:

==================
Hacking on BERadio
==================


Development and Deployment
==========================

``BERadio`` is hosted at:

    https://git.elmyra.de/hiveeyes/beradio

It is currently hot-deployed to its location at ``~/hiveeyes/serial-to-mqtt`` on ``einsiedlerkrebs.ddns.net`` using ``git``.
Feel welcome to hack away on it in this place. You can get access to our shared ``ha-devs`` environment by sharing your
ssh public keys with us. There will be some updates coming to improve the overall robustness and flexibility.


Documentation generation and publishing
=======================================
To build html documentation locally, just run::

    make docs-html

    # open in browser
    open doc/build/html/index.html


Wire protocol
=============

The most common thing to amend is probably the definition of message fields received via ``BERadio``,
which implicitly establishes the mapping while decoding raw payloads.

Find its definition in ``src/hiveeyes.py``, lines 9 ff.::

    class HiveeyesWireProtocol(object):

        # "Bencode-over-Radio" field names, order matters.
        # implicitly establishes struct-mapping while decoding raw payloads.
        fieldnames = [
            'network_id', 'node_id', 'gateway_id',
            'temp1', 'temp2', 'temp3', 'temp4',
        ]

And the topic publishing in lines  66 ff.::

    class HiveeyesPublisher(object):

        # [...]

        # publish to different topics
        self.channel.publish_field(data, 'temp1')
        self.channel.publish_field(data, 'temp2')
        self.channel.publish_field(data, 'temp3')
        self.channel.publish_field(data, 'temp4')


MQTT topic computing
====================

The second most common thing to amend is probably the way how topic names are computed.

Find its definition in ``src/mqtt.py`` lines 45 ff.::

    class MQTTPublisher(object):

        # [...]

        def publish_point(self, name, value, data):
            topic = '{topic}/{network_id}/{gateway_id}/{node_id}/{name}'.format(topic=self.topic, name=name, **data)
            self.publish(topic, value)

Regarding topic naming, please have a look at :ref:`mqtt-resources`.

