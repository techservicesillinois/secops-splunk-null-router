import json

import pytest

from unittest.mock import patch, Mock

from phsoar_null_router.soar_null_router_connector import (
    Soar_Null_RouterConnector
)
from bhr_client.rest import Client as BHRClient


def _test_connectivity(fake_connector: Soar_Null_RouterConnector):
    in_json = {
        "appid": "fceeaac1-8f96-46d6-9c3b-896e363eb004",
        "identifier": "test_connectivity",
        "parameters": [{}]
    }

    # Execute Action
    action_result_str = fake_connector._handle_action(json.dumps(in_json), None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["message"] == "Active connection"


@patch("phsoar_null_router.soar_null_router_connector.login_from_env")
def test_connectivity(mock, fake_connector: Soar_Null_RouterConnector):
    mock.return_value = Mock(spec=BHRClient)
    _test_connectivity(fake_connector)
    mock.return_value.query.assert_called_once()


def test_connectivity_vcr(cassette, fake_connector: Soar_Null_RouterConnector):
    _test_connectivity(fake_connector)


def _test_block(fake_connector: Soar_Null_RouterConnector,
                cidr, source, why, duration, autoscale):
    in_json = {
        "appid": "fceeaac1-8f96-46d6-9c3b-896e363eb004",
        "identifier": "block",
        "parameters": [{
            "cidr": cidr,
            "source": source if source else 'SOAR',
            "why": why,
            "duration": duration if duration else '300',
            "autoscale": autoscale,
        }]
    }

    # Execute Action
    dump = json.dumps(in_json)
    action_result_str = fake_connector._handle_action(dump, None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["message"] == f"Blocked {cidr}"

    return in_json

@pytest.mark.parametrize("cidr,source,why,duration,autoscale", [
    ('151.45.29.79/32', 'TEST', "Malicious IP!", '100', "false"),
    ('151.45.29.20/32', '', "Malicious IP!", '', "true"),
])
@patch("phsoar_null_router.soar_null_router_connector.login_from_env")
def test_block(mock, fake_connector: Soar_Null_RouterConnector, cidr, source,
               why, duration, autoscale):
    mock.return_value = Mock(spec=BHRClient)
    in_json = _test_block(
        fake_connector,
        cidr,
        source,
        why,
        duration,
        autoscale
    )

    parameters = in_json['parameters'][0]
    if parameters["autoscale"] == "true":
        parameters["autoscale"] = True 
    else: 
        parameters["autoscale"] = False
    mock.return_value.block.assert_called_once_with(**parameters)


def test_block_vcr(cassette, fake_connector: Soar_Null_RouterConnector):
    _test_block(
        fake_connector,
        '151.45.29.79/32',
        'TEST',
        'Malicious IP!',
        '100',
        "false"
    )
