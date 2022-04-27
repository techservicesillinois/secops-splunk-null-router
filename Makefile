all: build

build:
	python -m compileall src
	tar -zcvf soar_null_router.tgz -C src .
