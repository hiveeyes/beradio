# ------------------------------------------
#                forwarders
# ------------------------------------------
forward:
	beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://localhost --protocol=1

forward-v2:
	beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://localhost --protocol=2


# TODO: refactor to counter growth, honor beradio-0.1 vs. beradio-0.2

forward-swarm:
	beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://swarm.hiveeyes.org --protocol=1

forward-swarm-v2:
	beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://swarm.hiveeyes.org --protocol=2



# ------------------------------------------
#                 pretenders
# ------------------------------------------

pretend-local:
	@.venv27/bin/python beradio/publish.py localhost li999ei99ei1ei2218ei2318ei2462ei2250ee

pretend-local-v2:
	beradio forward --source=data://li999ei99ei1ei2218ei2318ei2462ei2250ee --target=mqtt://localhost --protocol=2

pretend-local-random:
	@.venv27/bin/python beradio/publish.py localhost random

pretend-docker:
	@.venv27/bin/python beradio/publish.py 192.168.59.103 li999ei99ei1ei2218ei2318ei2462ei2250ee

pretend-docker-random:
	@.venv27/bin/python beradio/publish.py 192.168.59.103 random

pretend-swarm-v1:
	beradio forward --source=data://li999ei99ei1ei2218ei2318ei2462ei2250ee --target=mqtt://swarm.hiveeyes.org --protocol=1

pretend-swarm-v2:
	beradio forward --source=data://d1:tli3455ei3455ei3455ei3455ee1:hli890ei377ee1:wi12333ee --target=mqtt://swarm.hiveeyes.org --protocol=2

pretend-swarm-random-v1:
	@#.venv27/bin/python beradio/publish.py swarm.hiveeyes.org random
	beradio forward --source=data://random --target=mqtt://swarm.hiveeyes.org --protocol=1

pretend-swarm-random-v2:
	beradio forward --source=data://random --target=mqtt://swarm.hiveeyes.org --protocol=2



# ------------------------------------------
#                 utilities
# ------------------------------------------
virtualenv:
	test -e .venv27/bin/python || `command -v virtualenv` --python=`command -v python` --no-site-packages .venv27
	.venv27/bin/pip install -r requirements.txt

docs-html: virtualenv
	export SPHINXBUILD="`pwd`/.venv27/bin/sphinx-build"; cd doc; make html
