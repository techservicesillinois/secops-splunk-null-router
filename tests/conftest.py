import logging
import os
import pytest
import vcr

from urllib.parse import urlparse
from app.app import AppConnector  # type: ignore[attr-defined]

CASSETTE_HOSTNAME = "FOO"
VCR_RECORD = "VCR_RECORD" in os.environ

# Load pytest-splunk-soar-connectors plugin
pytest_plugins = ("splunk-soar-connectors")


@pytest.fixture
def connector(monkeypatch) -> AppConnector:
    conn = AppConnector()
    if not VCR_RECORD:  # Always use cassette values when using cassette
        monkeypatch.setenv('BHR_HOST', f'https://{CASSETTE_HOSTNAME}')
        monkeypatch.setenv('BHR_TOKEN', 'FAKE_TOKEN')
    conn.logger.setLevel(logging.INFO)
    return conn


def clean_request(request):
    request.uri = replace_hostname(request.uri, CASSETTE_HOSTNAME)
    return request


def clean_response(response):
    try:
        response["body"]["string"] = response["body"]["string"].replace(
            bytes(os.environ["BHR_HOST"].replace("https://", ""), "ascii"),
            bytes(CASSETTE_HOSTNAME, "ascii"))
    except KeyError:
        pass
    return response


def replace_hostname(url: str, hostname: str):
    return urlparse(url)._replace(netloc=hostname).geturl()


@pytest.fixture
def cassette(request) -> vcr.cassette.Cassette:
    my_vcr = vcr.VCR(
        cassette_library_dir='cassettes',
        before_record_request=clean_request,
        before_record_response=clean_response,
        record_mode='once' if VCR_RECORD else 'none',
        filter_headers=[('Authorization', 'Bearer FAKE_TOKEN')]
    )

    with my_vcr.use_cassette(f'{request.function.__name__}.yaml') as tape:
        yield tape

        if my_vcr.record_mode == 'none':  # Tests only valid when not recording
            assert tape.all_played, \
                f"Only played back {len(tape.responses)} responses"
            assert tape.play_count == 1
