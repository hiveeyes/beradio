# Miscellaneous tools:
# Software tests, Documentation builder, Virtual environment builder


# ------
# Common
# ------

$(eval venvpath     := `pwd`/.venv27)
$(eval pip          := $(venvpath)/bin/pip)
$(eval python       := $(venvpath)/bin/python)
$(eval bumpversion  := $(venvpath)/bin/bumpversion)
$(eval twine        := $(venvpath)/bin/twine)
$(eval sphinx       := $(venvpath)/bin/sphinx-build)
$(eval nose2        := $(venvpath)/bin/nose2)

setup-virtualenv:
	@test -e $(python) || `command -v virtualenv` --python=`command -v python` --no-site-packages $(venvpath)


# -------
# Testing
# -------

setup-test: setup-virtualenv
	@$(pip) install --quiet --editable .[test]

test: setup-test
	@$(nose2)                   \
		$(options)              \
		--verbose               \
		beradio

test-cover:
	$(MAKE) test options="--with-coverage --coverage-report=term-missing"

#	--with-doctest --doctest-tests --doctest-extension=rst \
#	--with-coverage --cover-package=beradio --cover-tests \
#	--cover-html --cover-html-dir=coverage/html --cover-xml --cover-xml-file=coverage/coverage.xml


# -------------
# Documentation
# -------------

setup-docs: setup-virtualenv
	$(pip) install --quiet --requirement requirements-docs.txt

docs-html: setup-docs
	$(python) setup.py --quiet develop
	touch doc/source/index.rst
	export SPHINXBUILD="$(sphinx)"; cd doc; make html


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
