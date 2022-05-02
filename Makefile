all: build

build:
	python -m compileall src
	tar -zcvf soar_null_router.tgz -C src .

clean:
	rm -f soar_null_router.tgz
