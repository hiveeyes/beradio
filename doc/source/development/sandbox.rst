.. _sandbox:

#############
Sandbox setup
#############

Setup Mosquitto MQTT broker
---------------------------

Run Mosquitto on Docker, for development on Mac OS X.
https://github.com/toke/docker-mosquitto

First time::

    boot2docker up
    eval "$(boot2docker shellinit)"
    docker run -tip 1883:1883 -p 9001:9001 --name=mosquitto toke/mosquitto

Regular::

    boot2docker up
    eval "$(boot2docker shellinit)"
    docker start mosquitto

Inquire IP address from boot2docker host::

    boot2docker ip
    192.168.59.103
