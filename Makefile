# ==========================================
#                BERadio v2
# ==========================================


# ------------------------------------------
#                forwarders
# ------------------------------------------
forward:
	beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://localhost --protocol=2

forward-swarm:
	beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://swarm.hiveeyes.org --protocol=2


# ------------------------------------------
#                subscribers
# ------------------------------------------
subscribe-local:
	bemqtt subscribe --source=mqtt://localhost

subscribe-docker:
	bemqtt subscribe --source=mqtt://192.168.59.103

subscribe-swarm:
	bemqtt subscribe --source=mqtt://swarm.hiveeyes.org



# ------------------------------------------
#                pretenders
# ------------------------------------------
#
# publish static or random data to MQTT
#
pretend-local:
	beradio forward --source=data://d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee --target=mqtt://localhost --protocol=2

pretend-local-random:
	beradio forward --source=data://random --target=mqtt://localhost --protocol=2

pretend-docker:
	beradio forward --source=data://d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee --target=mqtt://192.168.59.103 --protocol=2

pretend-docker-random:
	beradio forward --source=data://random --target=mqtt://192.168.59.103 --protocol=2

pretend-swarm:
	beradio forward --source=data://d1:#i999e1:_2:h11:hli488ei572ee1:tli2163ei1925ei1092ei1354ee1:wi10677ee --target=mqtt://swarm.hiveeyes.org --protocol=2

pretend-swarm-random:
	beradio forward --source=data://random --target=mqtt://swarm.hiveeyes.org --protocol=2



# ==========================================
#                BERadio v1
# ==========================================
forward-v1:
	beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://localhost --protocol=1

forward-swarm-v1:
	beradio forward --source=serial:///dev/ttyUSB0 --target=mqtt://swarm.hiveeyes.org --protocol=1

pretend-local-v1:
	@.venv27/bin/python beradio/publish.py localhost li999ei99ei1ei2218ei2318ei2462ei2250ee

pretend-local-random-v1:
	@.venv27/bin/python beradio/publish.py localhost random

pretend-docker-v1:
	@.venv27/bin/python beradio/publish.py 192.168.59.103 li999ei99ei1ei2218ei2318ei2462ei2250ee

pretend-docker-random-v1:
	@.venv27/bin/python beradio/publish.py 192.168.59.103 random

pretend-swarm-v1:
	beradio forward --source=data://li999ei99ei1ei2218ei2318ei2462ei2250ee --target=mqtt://swarm.hiveeyes.org --protocol=1

pretend-swarm-random-v1:
	@#.venv27/bin/python beradio/publish.py swarm.hiveeyes.org random
	beradio forward --source=data://random --target=mqtt://swarm.hiveeyes.org --protocol=1



# ==========================================
#                 utilities
# ==========================================

# ------------------------------------------
#                   misc
# ------------------------------------------
#
# Miscellaneous tools:
# Software tests, Documentation builder, Virtual environment builder
#
test: virtualenv
	@# https://nose.readthedocs.org/en/latest/plugins/doctests.html
	@# https://nose.readthedocs.org/en/latest/plugins/cover.html
	nosetests --with-doctest --doctest-tests --doctest-extension=rst

test-coverage: virtualenv
	nosetests \
		--with-doctest --doctest-tests --doctest-extension=rst \
		--with-coverage --cover-package=beradio --cover-tests \
		--cover-html --cover-html-dir=coverage/html --cover-xml --cover-xml-file=coverage/coverage.xml

docs-html: virtualenv
	export SPHINXBUILD="`pwd`/.venv27/bin/sphinx-build"; cd doc; make html

virtualenv:
	@test -e .venv27/bin/python || `command -v virtualenv` --python=`command -v python` --no-site-packages .venv27
	@.venv27/bin/pip --quiet install --requirement requirements-dev.txt


# ------------------------------------------
#                 releasing
# ------------------------------------------
#
# Release targets for convenient release cutting.
#
# Synopsis::
#
#    make release bump={patch,minor,major}
#

bumpversion:
	bumpversion $(bump)

push:
	git push && git push --tags

sdist:
	python setup.py sdist

upload:
	rsync -auv ./dist/beradio-*.tar.gz hiveeyes@packages.elmyra.de:/srv/packages/customers/hiveeyes/python/eggs/beradio/

release: virtualenv bumpversion push sdist upload
