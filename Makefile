.PHONY: all build clean lint static
SRCS_DIR:=src/phsoar_null_router
TSCS_DIR:=tests
SOAR_SRCS:=$(shell find $(SRCS_DIR) -type f)
SRCS:=$(shell find $(SRCS_DIR) -name '*.py')
TSCS:=$(shell find $(TSCS_DIR) -name '*.py')
VERSION_FILES:=$(addprefix $(SRCS_DIR)/, soar_null_router.json soar_null_router_connector.py)
GITHUB_DEPLOYED:=$(shell date -u +%FT%X.%6NZ)
VENV_PYTHON:=venv/bin/python
VENV_REQS:=.requirements.venv

ifeq (tag, $(GITHUB_REF_TYPE))
	TAG?=$(GITHUB_REF_NAME)
else
	TAG?=0.0.0
endif

all: build

build: soar_null_router.tgz

soar_null_router.tgz: .tag .commit .deployed $(SOAR_SRCS)
	tar zcvf $@ -C src .

version: .tag .commit .deployed
.tag: $(VERSION_FILES)
	echo version $(TAG)
	sed -i s/GITHUB_TAG/$(TAG)/ $^
	touch $@
.commit: $(VERSION_FILES)
	echo commit $(GITHUB_SHA)
	sed -i s/GITHUB_SHA/$(GITHUB_SHA)/ $^
	touch $@
.deployed: $(VERSION_FILES)
	echo deployed $(GITHUB_DEPLOYED)
	sed -i s/GITHUB_DEPLOYED/$(GITHUB_DEPLOYED)/ $^
	touch $@

deploy: soar_null_router.tgz
	python deploy.py

venv: requirements-test.txt
	python -m venv venv
	$(VENV_PYTHON) -m pip install -r $^

requirements-test.txt: export PYTEST_SOAR_REPO=git+ssh://git@github.com/edthedev/pytest-splunk-soar-connectors.git
requirements-test.txt: requirements-test.in
	rm -rf $(VENV_REQS)
	python -m venv $(VENV_REQS)
	$(VENV_REQS)/bin/python -m pip install -r $^
	$(VENV_REQS)/bin/python -m pip freeze -qqq > $@
	#REMOVE once pytest-splunk-soar-connectors is on pypi
	sed -i "s;^pytest-splunk-soar-connectors==.*;$(PYTEST_SOAR_REPO);" $@

lint: .lint
.lint: $(SRCS) $(TSCS)
	$(VENV_PYTHON) -m flake8 $?
	touch $@

static: .static
.static: $(SRCS) $(TSCS)
	$(VENV_PYTHON) -m mypy $?
	touch $@

test: venv lint static
	$(VENV_PYTHON) -m pytest
	
clean:
	rm -rf venv $(VENV_REQS)
	rm -rf .lint .static
	rm -f soar_null_router.tgz .tag
	-find src -type d -name __pycache__ -exec rm -fr "{}" \;
	git checkout -- $(TAG_FILES)

force-clean: clean
	rm -f requirements-test.txt
