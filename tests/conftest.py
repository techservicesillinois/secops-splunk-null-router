import logging
import pytest
import vcr

from app.app import AppConnector

# Load pytest-splunk-soar-connectors plugin
pytest_plugins = ("splunk-soar-connectors")


def _connector():
    conn = AppConnector()
    conn.logger.setLevel(logging.INFO)
    return conn


@pytest.fixture(scope='function')
def connector():
    return _connector()


@pytest.fixture(scope='function')
def fake_connector(monkeypatch):
    monkeypatch.setenv('BHR_HOST', 'https://nr-test.techservices.illinois.edu')
    monkeypatch.setenv('BHR_TOKEN', 'FAKE_TOKEN')

    return _connector()


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
