virtualenv:
	virtualenv-2.7 --no-site-packages .venv27

forward:
	@.venv27/bin/python src/serial_to_mqtt.py /dev/ttyUSB0 localhost

pretend:
	@.venv27/bin/python src/publish.py 192.168.59.103 li999ei99ei1ei2218ei2318ei2462ei2250ee

pretend-elbanco:
	@.venv27/bin/python src/publish.py elbanco.hiveeyes.org li999ei99ei1ei2218ei2318ei2462ei2250ee
