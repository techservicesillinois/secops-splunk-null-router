.PHONY: all build clean

all: build

build: soar_null_router.tgz

soar_null_router.tgz:
#	python -m compileall -b src
	tar -zcvf $@ -C src .

deploy: soar_null_router.tgz
	python deploy.py
clean:
	rm -f soar_null_router.tgz
	rm -rf src/__pycache__
