# Contributing

## Release Instructions
    1. Merge an update to main with a new release number in the .json file. 
    2. Have someone from SecOps change the version in the Splunk SOAR interface.

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements-test.txt
```

> You may need to `pip install wheel` then re-run
> `pip install -r requirements-test.txt` to clear a `bdist_wheel` error message.


```shell
export BHR_HOST="https://nr-test.techservices.illinois.edu"
export BHR_TOKEN=
```

## VCR.py is used for testing http requests 
https://vcrpy.readthedocs.io/en/latest/
