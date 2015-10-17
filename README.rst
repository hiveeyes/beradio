=====================
serial-to-mqtt README
=====================

Setup application
=================
- Install Python dependencies::

    aptitude install python-virtualenv
    virtualenv --system-site-packages .venv27
    source .venv27/bin/activate

    # pyserial, mosquitto, bencode
    pip install -r requirements.txt


Run forwarder
=============

Publish serial data to MQTT broker running on the same machine::

    make forward


Run pretend publisher
=====================

Publish fixed data to MQTT broker running inside a Docker container::

    make pretend


Run MQTT subscriber
===================
- MQTTLens: https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm/related?hl=en
