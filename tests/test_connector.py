import json
import os
import sys
from urllib.error import HTTPError

import pytest
import vcr

from unittest.mock import patch, Mock
from requests.exceptions import HTTPError

from phsoar_null_router.soar_null_router_connector import Soar_Null_RouterConnector
from bhr_client.rest import Client as BHRClient

@patch("phsoar_null_router.soar_null_router_connector.login_from_env")
def test_connectivity(mock, connector: Soar_Null_RouterConnector):
    mock.return_value = Mock(spec=BHRClient)
    in_json = {
            "appid": "fceeaac1-8f96-46d6-9c3b-896e363eb004",
            "parameters": {
                "identifier": "test_connectivity",
            }
    }

    # Execute Action
    action_result_str = connector._handle_action(json.dumps(in_json), None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["message"] == "Active connection"
    mock.return_value.query.assert_called_once()

@patch("phsoar_null_router.soar_null_router_connector.login_from_env")
def test_block(mock, connector: Soar_Null_RouterConnector):
    cidr='192.0.2.1/32'

    mock.return_value = Mock(spec=BHRClient)
    in_json = {
            "appid": "fceeaac1-8f96-46d6-9c3b-896e363eb004",
            "parameters": {
                "identifier": "block",
                "cidr": cidr,
            }
    }

    # Execute Action
    dump = json.dumps(in_json)
    action_result_str = connector._handle_action(dump, None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["message"] == f"Blocked {cidr}"
    mock.return_value.block.assert_called_once_with(
        cidr='192.0.2.1/32',
        source='SOAR', 
        why='Appears in our suspicious event list.')

#@vcr.use_cassette('cassettes/test_connectivity_fail.yaml', record_mode='once')
def test_connectivity_fail(connector: Soar_Null_RouterConnector):
#def test_connectivity_fail(cassette, connector: Soar_Null_RouterConnector):
    in_json = {
            "appid": "fceeaac1-8f96-46d6-9c3b-896e363eb004",
            "parameters": {
                "identifier": "test_connectivity",
            }
    }

    with vcr.use_cassette('tests/cassettes/test_connectivity_fail.yaml') as cassette:
        with pytest.raises(HTTPError):
            action_result_str = connector._handle_action(json.dumps(in_json), None)

        assert cassette.all_played
        assert cassette.play_count == 1
