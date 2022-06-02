# Contributing

## Release Instructions
    1. Merge an update to main with a new release number in the .json file. 
    2. Have someone from SecOps change the version in the Splunk SOAR interface.

## Setup

Python version should be set to 3.9 to match Splunk SOAR.

```shell
pyenv install 3.9.0
pyenv local 3.9.0
```

You can verify the above with `python --version`:
```
$ python --version
Python 3.9.0
```

```shell
make clean venv
source venv/bin/activate
```

> You may need to `pip install wheel` then re-run
> `pip install -r requirements-test.txt` to clear a `bdist_wheel` error message.

For integration testing, set BRH environment variables as used by `bhr-client`.

```shell
export BHR_HOST="https://nr-test.techservices.illinois.edu"
export BHR_TOKEN=
```

## Updating Library Versions

```shell
make clean
make requirements-test.txt
```

## VCR.py is used for testing http requests 
https://vcrpy.readthedocs.io/en/latest/
