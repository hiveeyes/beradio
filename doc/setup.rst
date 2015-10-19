====================
serial-to-mqtt setup
====================


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



More MQTT software
==================
- | MQTTLens
  | https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm/related?hl=en
- | D3 MQTT TOPIC TREE VISUALISER
  | http://www.hardill.me.uk/wordpress/2012/11/08/d3-mqtt-topic-tree-visualiser/
  | http://www.hardill.me.uk:3000/
  | https://harizanov.com/2014/09/mqtt-topic-tree-structure-improvements/
- | mqttwarn: a pluggable MQTT notifier
  | https://github.com/jpmens/mqttwarn
  | http://jpmens.net/2014/02/17/introducing-mqttwarn-a-pluggable-mqtt-notifier/
  | http://shortcircuit.net.au/~prologic/blog/article/2014/02/28/mqtt-python-pluggable-notifications-mqttwarn/
- | mqttcollect: MQTT-based Exec-plugin for collectd
  | https://github.com/jpmens/mqttcollect
  | http://jpmens.net/2015/05/15/an-exec-plugin-for-collectd-mqttcollect/
