======================
serial-to-mqtt hacking
======================


Development and Deployment
==========================

``serial-to-mqtt`` is hosted at:

    https://git.elmyra.de/hiveeyes/serial-to-mqtt

It is currently hot-deployed to its location at ``~/hiveeyes/serial-to-mqtt`` on ``einsiedlerkrebs.ddns.net`` using ``git``.
Feel welcome to hack away on it in this place. You can get access to our shared ``ha-devs`` environment by sharing your ssh public keys with us. There will be some updates coming to improve the overall robustness and flexibility.


Wire protocol
=============

The most common thing to amend is probably the definition of message fields received via ``Bencode-over-RFM69`` (we need a catchy name for that, see ``Firmata`` etc.), which implicitly establishes the mapping while decoding raw payloads.

Find its definition in ``src/hiveeyes.py``::

    class HiveeyesWireProtocol(object):

        # "Bencode-over-RFM69" field names, order matters.
        # implicitly establishes struct-mapping while decoding raw payloads.
        fieldnames = [
            'network_id', 'node_id', 'gateway_id',
            'temp1', 'temp2', 'temp3', 'temp4',
        ]
