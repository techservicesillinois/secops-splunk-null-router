# Contributing

## Release Instructions

    1. Merge an update to main with a new release number in the .json file. 
    2. Have someone from SecOps change the version in the Splunk SOAR interface.

## Setup

Python version should be set to 3.9 to match Splunk SOAR:

    ```shell
    pyenv install 3.9.0
    pyenv local 3.9.0
    ```

You can verify the above with `python --version`:

    ```shell
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
    $ make force-clean requirements-test.txt
    ```

## Testing

[VCR.py][48] is used for testing http requests.

[48]: https://vcrpy.readthedocs.io/en/latest/

> WARNING: The Null Router API can return a `500` error when sent a CIDR that it cannot block (i.e. a campus internal IP).

You can also test using version 0.0.0 in the Splunk web interface.

> WARNING: When running a test from the `Actions` web panel while viewing
> a Splunk SOAR app, the test will not run on the `automation broker` -
> even if the selected `asset` is set to use the automation broker.
> To test using the automation broker through the SOAR site, select an event and launch the action from it.
