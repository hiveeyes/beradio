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

To automatically publish documentation to https://docs.elmyra.de/hiveeyes/beradio, follow these steps:

- Add or enable key ``www-data@pulp`` at https://git.elmyra.de/hiveeyes/beradio/deploy_keys::

    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDEq0S3KQd22iuuHsdBPAdHctew89ex+RXtc6f0YJZSVtNyl0HCU7RdcDadNQA7muixJqVrZdOaz+YfC3InZt/6JMyhCfdwQNlsXuEH9QNfnll33bHeFCRJBayRub5BSzFF8gFs2VFDyqw1xj657NPp8BteXXiJiF1rCwAXrwPk4LA8PJwL3xCfZcrgBT8nTSzrK5ez/vM+sUKWE6SM+PRO9CljezO8z8vzi9qWoYWfsi5x/q4TO8xTiY6+v1FQKfJp0lggphfUFHmvkx1nvZofLXYdqXwLTPQJxpX7/i/rHL7kRh1cBI5UBZyEYzZ14p00iB+DHb89XO2XcacrCFiY4bakeVy652S47K21Hd8lRTVrKPeVuEcAyc+QhAu262V5N1Op1Ab/pZvDVVgeDXXUktT8DHvwPYtEEX3hEPsQMZHKu8ngedo4pavMqHqDTo2QF9VY5e53BaSkhRGfUOUv0Olm0TW5mzWMTbPLyzoYSTFeT0l+4zVHJNcEoxsSRPqcgaq03GFK2t/j+Mn69JwFCvB555cQ53SYR8o54QEn697Oxfv0G+ZSVS2d69hBV+XNz6BVXpBI0QCOS7tTehHokNODsgJHWJFp6+ueNWr+LWFj+8Q164IoMTtf4wym89A3wF/Bf7/474KC3xjW8NSoCC9+TcJc6RRW1rlQzjv8tQ== www-data@pulp

- Add web hook for "Push events" at https://git.elmyra.de/hiveeyes/beradio/hooks with URL::

    https://gitlab:KoabMulp@docs.elmyra.de/hiveeyes/.gitlab-webhook


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

Regarding topic naming, please have a look at `<mqtt.rst>`__.


