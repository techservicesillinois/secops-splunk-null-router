import logging
import os
import pytest
import vcr

# from urllib.parse import urlparse
from phsoar_null_router.soar_null_router_connector import (
    Soar_Null_RouterConnector
)

CASSETTE_TOKEN = "FAKE_TOKEN"
CASSETTE_HOST = "FOO"

# To record, `export VCR_RECORD=True`
VCR_RECORD = "VCR_RECORD" in os.environ

# Load pytest-splunk-soar-connectors plugin
pytest_plugins = ("splunk-soar-connectors")


@pytest.fixture
def connector() -> Soar_Null_RouterConnector:
    conn = Soar_Null_RouterConnector()
    if not VCR_RECORD:  # Always use cassette values when using cassette
        conn.config = {
            'BHR_HOST': CASSETTE_HOST,
            'BHR_TOKEN': CASSETTE_TOKEN,
        }
    else:  # User environment values
        env_keys = ['host', 'token']

        for key in env_keys:
            env_key = f'BHR_{key.upper()}'
            conn.config[key] = os.environ.get(env_key, None)
            if not conn.config[key]:
                raise ValueError(f'{env_key} unset or empty with record mode')

    conn.logger.setLevel(logging.INFO)
    return conn


@pytest.fixture
def cassette(request) -> vcr.cassette.Cassette:
    my_vcr = vcr.VCR(
        cassette_library_dir='cassettes',
        record_mode='once' if VCR_RECORD else 'none',
        filter_headers=[('Authorization', 'Bearer FAKE_TOKEN')]
    )

    with my_vcr.use_cassette(f'{request.function.__name__}.yaml') as tape:
        yield tape

        if my_vcr.record_mode == 'none':  # Tests only valid when not recording
            assert tape.all_played, \
                f"Only played back {len(tape.responses)} responses"
