# ------
# Common
# ------

setup-virtualenv:
	@test -e .venv27/bin/python || `command -v virtualenv` --python=`command -v python` --no-site-packages .venv27


# -------
# Testing
# -------

# Miscellaneous tools:
# Software tests, Documentation builder, Virtual environment builder

setup-test: setup-virtualenv
	@.venv27/bin/pip install --quiet --editable .[test]

test: setup-test
	nosetests

test-coverage: setup-test
	nosetests \
		--with-doctest --doctest-tests --doctest-extension=rst \
		--with-coverage --cover-package=beradio --cover-tests \
		--cover-html --cover-html-dir=coverage/html --cover-xml --cover-xml-file=coverage/coverage.xml


# -------------
# Documentation
# -------------

setup-docs: setup-virtualenv
	@.venv27/bin/pip install --quiet --requirement requirements-docs.txt

docs-html: setup-virtualenv
	`pwd`/.venv27/bin/python setup.py --quiet develop
	touch doc/source/index.rst
	export SPHINXBUILD="`pwd`/.venv27/bin/sphinx-build"; cd doc; make html


# ---------
# Releasing
# ---------
#
# Release targets for convenient release cutting.
#
# Synopsis::
#
#    make release bump={patch,minor,major}
#

setup-release: setup-virtualenv
	@.venv27/bin/pip install --quiet --requirement requirements-release.txt

bumpversion:
	bumpversion $(bump)

push:
	git push && git push --tags

sdist:
	python setup.py sdist

upload:
	@#rsync -auv ./dist/beradio-*.tar.gz hiveeyes@packages.hiveeyes.org:/srv/packages/organizations/hiveeyes/python/eggs/beradio/
	twine upload --skip-existing dist/*.tar.gz

release: setup-virtualenv bumpversion push sdist upload
