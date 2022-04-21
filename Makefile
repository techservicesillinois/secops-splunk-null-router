.PHONY: all build clean
SRCS_DIR:=src/phsoar_null_router
SRCS:=$(shell find $(SRCS_DIR) -type f)
TAG_FILES:=$(addprefix $(SRCS_DIR)/, soar_null_router.json __init__.py)

all: build

build: soar_null_router.tgz

soar_null_router.tgz: .tag $(SRCS)
	tar zcvf $@ -C src .

version: .tag
.tag: $(TAG_FILES)
	echo version $$GITHUB_REF_NAME
	sed -i s/GITHUB_TAG/$(GITHUB_REF_NAME)/ $^
	touch $@

deploy: soar_null_router.tgz
	python deploy.py

clean:
	rm -f soar_null_router.tgz .tag
	find src -type d -name __pycache__ -exec rm -fr "{}" \;
	git checkout -- $(TAG_FILES)
