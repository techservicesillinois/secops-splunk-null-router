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
def connector(monkeypatch) -> Soar_Null_RouterConnector:
    conn = Soar_Null_RouterConnector()
    monkeypatch.setenv('BHR_HOST', 'https://nr-test.techservices.illinois.edu')
    monkeypatch.setenv('BHR_TOKEN', 'FAKE_TOKEN')
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
