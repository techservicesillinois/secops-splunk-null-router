.PHONY: all build clean
SRCS_DIR:=src/phsoar_null_router
SRCS:=$(shell find $(SRCS_DIR) -type f)
TAG_FILES:=$(addprefix $(SRCS_DIR)/, soar_null_router.json __init__.py)
VENV_PYTHON:=venv/bin/python

ifeq (tag, $(GITHUB_REF_TYPE))
	TAG?=$(GITHUB_REF_NAME)
else
	TAG?=0.0.0
endif

all: build

build: soar_null_router.tgz

soar_null_router.tgz: .tag $(SRCS)
	tar zcvf $@ -C src .

version: .tag
.tag: $(TAG_FILES)
	echo version $(TAG)
	sed -i s/GITHUB_TAG/$(TAG)/ $^
	touch $@

deploy: soar_null_router.tgz
	python deploy.py

clean:
	rm -rf venv
	rm -f soar_null_router.tgz .tag
	-find src -type d -name __pycache__ -exec rm -fr "{}" \;
	git checkout -- $(TAG_FILES)

venv:
	python -m venv venv
	$(VENV_PYTHON) -m pip install wheel
	$(VENV_PYTHON) -m pip install -r requirements-test.txt

test: venv
	$(VENV_PYTHON) -m pytest
