import json
import os
import sys
import logging
import pytest
import vcr

from phsoar_null_router.soar_null_router_connector import (
    Soar_Null_RouterConnector
)

# Load pytest-splunk-soar-connectors plugin
pytest_plugins = ("splunk-soar-connectors")


@pytest.fixture(scope='function')
def connector(monkeypatch):
    monkeypatch.setenv('BHR_HOST', 'https://nr-test.techservices.illinois.edu')
    monkeypatch.setenv('BHR_TOKEN', 'FAKE_TOKEN')

    conn = Soar_Null_RouterConnector()
    conn.logger.setLevel(logging.INFO)
    return conn


@pytest.fixture
def cassette(request) -> vcr.cassette.Cassette:
    my_vcr = vcr.VCR(
        cassette_library_dir='cassettes',
        record_mode='none',
        filter_headers=[('Authorization', 'Bearer FAKE_TOKEN')]
    )

    with my_vcr.use_cassette(f'{request.function.__name__}.yaml') as tape:
        yield tape
        assert tape.all_played
        assert tape.play_count == 1
