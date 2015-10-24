=========
MQTT misc
=========

MQTT topic naming
-----------------

Regarding topic naming, please consider in general

> There are only two hard things in Computer Science: cache invalidation and naming things.
>   -- Phil Karlton
>
> http://martinfowler.com/bliki/TwoHardThings.html


and have a look at these fine readings:

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
  | https://www-01.ibm.com/support/knowledgecenter/SSFKSJ_7.1.0/com.ibm.mq.doc/tt60310_.htm



Various readings
----------------
- https://www.npmjs.com/package/mqtt-bridge
- http://mqtt.org/2011/08/mqtt-and-android-make-great-partners
- http://2lemetry.com/2014/10/24/avoiding-mqtt-pitfalls/
- | Playing with MQTT
  | http://mmtn.borioli.net/?p=1342


Mosquitto history
-----------------
- https://www.ibm.com/developerworks/community/groups/service/html/communityview?communityUuid=d5bedadd-e46f-4c97-af89-22d65ffee070
- http://projects.eclipse.org/projects/technology.mosquitto
- http://mosquitto.org/


Other MQTT software
-------------------
- | Paho
  | The Paho project provides open-source client implementations of MQTT and MQTT-SN messaging protocols aimed at new,
  | existing, and emerging applications for Machine‑to‑Machine (M2M) and Internet of Things (IoT).
  | https://eclipse.org/paho/
  | https://pypi.python.org/pypi/paho-mqtt
  | https://eclipse.org/paho/clients/python/

- | WebSphere MQ Telemetry
  | http://www-03.ibm.com/software/products/en/wmq-telemetry
  | http://www.redbooks.ibm.com/abstracts/tips0876.html
  | http://www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/SG248054.html
  | https://www.ibm.com/developerworks/community/blogs/aimsupport/entry/whats_new_in_websphere_mq_explorer_v75?lang=en
  | https://stackoverflow.com/questions/15366203/websphere-mq-explorer-does-not-show-queues-after-successful-connection
  | https://hursleyonwmq.wordpress.com/2007/02/08/using-websphere-mq-explorer-as-a-read-only-viewer/

- | mqtt_fuzz
  | https://github.com/F-Secure/mqtt_fuzz
