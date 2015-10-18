virtualenv:
	virtualenv-2.7 --no-site-packages .venv27

forward:
	@.venv27/bin/python src/serial_to_mqtt.py /dev/ttyUSB0 localhost


# refactor to counter growth

forward-swarm:
	@.venv27/bin/python src/serial_to_mqtt.py /dev/ttyUSB0 swarm.hiveeyes.org

pretend-local:
	@.venv27/bin/python src/publish.py localhost li999ei99ei1ei2218ei2318ei2462ei2250ee

pretend-local-random:
	@.venv27/bin/python src/publish.py localhost random

pretend-docker:
	@.venv27/bin/python src/publish.py 192.168.59.103 li999ei99ei1ei2218ei2318ei2462ei2250ee

pretend-docker-random:
	@.venv27/bin/python src/publish.py 192.168.59.103 random

pretend-swarm:
	@.venv27/bin/python src/publish.py swarm.hiveeyes.org li999ei99ei1ei2218ei2318ei2462ei2250ee

pretend-swarm-random:
	@.venv27/bin/python src/publish.py swarm.hiveeyes.org random
