.. _mqtt-resources:

###############
Everything MQTT
###############

.. _mqtt-topic-naming:

*****************
MQTT topic naming
*****************

Intro
=====

Regarding topic naming, please consider in general

.. epigraph::

    There are only two hard things in Computer Science: cache invalidation and naming things. `[1] <http://martinfowler.com/bliki/TwoHardThings.html>`_

    -- Phil Karlton


Articles
========
... and have a look at these fine readings:

Readings I
----------
- http://tinkerman.eldiariblau.net/mqtt-topic-naming-convention/
- http://blog.hekkers.net/2012/09/18/mqtt-about-dumb-sensors-topics-and-clean-code/
- http://lodge.glasgownet.com/2012/09/23/mqtt-republishing-itch/
- https://github.com/kylegordon/mqtt-republisher
- | topics, brokers, mount_points, and light bulbs, oh my
  | https://groups.google.com/forum/?fromgroups=#!topic/mqtt/wk3MhXKYIZA
- http://www.embedded.com/electronics-blogs/embedded-cloud-talkers/4397229/Device-to-Cloud--
- https://developer.ibm.com/answers/questions/193326/mqtt-bridge-to-iotf.html
- | MQTT Spec, Version 3.1.1
  | 4.7 Topic Names and Topic Filters
  | http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718106
- | Using JSON Data and choosing topic names
  | http://forum.pidome.org/viewtopic.php?id=10


Also, when thinking about addressing, don't forget about "MQTT client identifier":

- | The MQTT client identifier
  | `<https://www-01.ibm.com/support/knowledgecenter/SSFKSJ_7.1.0/com.ibm.mq.doc/tt60310_.htm>`_


Readings II
-----------
- https://www.npmjs.com/package/mqtt-bridge
- http://mqtt.org/2011/08/mqtt-and-android-make-great-partners
- http://2lemetry.com/2014/10/24/avoiding-mqtt-pitfalls/
- | Playing with MQTT
  | http://mmtn.borioli.net/?p=1342
- https://blogs.vmware.com/vfabric/2013/02/choosing-your-messaging-protocol-amqp-mqtt-or-stomp.html


Mosquitto history
-----------------
- https://www.ibm.com/developerworks/community/groups/service/html/communityview?communityUuid=d5bedadd-e46f-4c97-af89-22d65ffee070
- http://projects.eclipse.org/projects/technology.mosquitto
- http://mosquitto.org/


*************
MQTT software
*************

Brokers
=======

- | Paho
  | The Paho project provides open-source client implementations of MQTT and MQTT-SN messaging protocols aimed at new,
  | existing, and emerging applications for Machine‑to‑Machine (M2M) and Internet of Things (IoT).
  | https://eclipse.org/paho/
  | https://pypi.python.org/pypi/paho-mqtt
  | https://eclipse.org/paho/clients/python/

- | RabbitMQ
  | https://www.rabbitmq.com/mqtt.html

- | WebSphere MQ Telemetry
  | http://www-03.ibm.com/software/products/en/wmq-telemetry
  | http://www.redbooks.ibm.com/abstracts/tips0876.html
  | http://www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/SG248054.html
  | https://www.ibm.com/developerworks/community/blogs/aimsupport/entry/whats_new_in_websphere_mq_explorer_v75?lang=en
  | https://stackoverflow.com/questions/15366203/websphere-mq-explorer-does-not-show-queues-after-successful-connection
  | https://hursleyonwmq.wordpress.com/2007/02/08/using-websphere-mq-explorer-as-a-read-only-viewer/


Clients
=======

Common
------
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
- | mqtt_fuzz
  | https://github.com/F-Secure/mqtt_fuzz

MQTT in the Browser
-------------------
- | Using MQTT.js in the browser over WebSocket
  | https://github.com/mcollina/mows
- | The MQTT client for Node.js and the browser
  | https://github.com/mqttjs/MQTT.js
- | Simple WebSockets Proxy for a MQTT broker, based on Twisted and Autobahn
  | https://gist.github.com/claws/8794715
  | https://github.com/crossbario/autobahn-python/blob/master/examples/twisted/websocket/wrapping/README.md


Embedded
========

C++
---
- | A client library for the Arduino Ethernet Shield that provides support for MQTT
  | http://pubsubclient.knolleary.net/
  | https://github.com/knolleary/pubsubclient
- https://github.com/adafruit/Adafruit_MQTT_Library
- | MQTT client library for ESP8266 Soc
  | https://github.com/tuanpmt/esp_mqtt
  | http://tuanpm.net/native-mqtt-client-library-for-esp8266/

Lua
---




Platforms
=========
- https://aws.amazon.com/iot/
    - https://aws.amazon.com/iot/how-it-works/
    - https://docs.aws.amazon.com/iot/latest/developerguide/protocols.html
- https://internetofthings.ibmcloud.com/
    - https://docs.internetofthings.ibmcloud.com/
    - https://docs.internetofthings.ibmcloud.com/reference/overview.html
    - https://docs.internetofthings.ibmcloud.com/messaging/payload.html
    - https://pypi.python.org/pypi/ibmiotc/
    - https://pypi.python.org/pypi/ibmiotf/
    - https://github.com/ibm-messaging/iot-python
