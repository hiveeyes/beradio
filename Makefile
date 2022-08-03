# Miscellaneous tools:
# Software tests, Documentation builder, Virtual environment builder


# ------
# Common
# ------

$(eval venvpath     := .venv)
$(eval pip          := $(venvpath)/bin/pip)
$(eval python       := $(venvpath)/bin/python)
$(eval bumpversion  := $(venvpath)/bin/bumpversion)
$(eval twine        := $(venvpath)/bin/twine)
$(eval sphinx       := $(venvpath)/bin/sphinx-build)
$(eval nose2        := $(venvpath)/bin/nose2)
$(eval coverage     := $(venvpath)/bin/coverage)
$(eval flake8       := $(venvpath)/bin/pflake8)
$(eval black        := $(venvpath)/bin/black)
$(eval isort        := $(venvpath)/bin/isort)
$(eval proselint    := $(venvpath)/bin/proselint)


setup-virtualenv:
	@test -e $(python) || python3 -m venv $(venvpath)
	@$(pip) install wheel


# -------
# Testing
# -------

setup-test: setup-virtualenv
	@$(pip) install --editable=.[test]

test: setup-test
	@$(nose2)                   \
		$(options)              \
		--verbose               \
		beradio

test-coverage:
	$(MAKE) test options="--with-coverage --coverage-report=term-missing"
	$(coverage) xml

#	--with-doctest --doctest-tests --doctest-extension=rst \
#	--with-coverage --cover-package=beradio --cover-tests \
#	--cover-html --cover-html-dir=coverage/html --cover-xml --cover-xml-file=coverage/coverage.xml


# -------------
# Documentation
# -------------

setup-docs: setup-virtualenv
	$(pip) install --requirement=requirements-docs.txt

docs-html: setup-docs
	@$(pip) install --editable=.
	touch doc/source/index.rst
	export SPHINXBUILD="$(shell pwd)/$(sphinx)"; cd doc; make html


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
	$(pip) install --requirement=requirements-release.txt

bumpversion:
	$(bumpversion) $(bump)

push:
	git push && git push --tags

build:
	$(python) -m build

upload:
	$(twine) upload --skip-existing dist/*{.tar.gz,.whl}

release: setup-release bumpversion push build upload



# ----------------------
# Formatting and linting
# ----------------------

format: setup-virtualenv
	$(pip) install --requirement=requirements-utils.txt
	$(black) .
	$(isort) .

lint: setup-virtualenv
	$(pip) install --requirement=requirements-utils.txt
	$(flake8) beradio testing
	$(proselint) *.rst doc/source/**/*.rst
