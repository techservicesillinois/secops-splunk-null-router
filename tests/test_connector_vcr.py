import json

import pytest

from phsoar_null_router.soar_null_router_connector import (
    Soar_Null_RouterConnector
)
from bhr_client.rest import Client as BHRClient


def test_connectivity_vcr(cassette, connector: Soar_Null_RouterConnector):
    in_json = {
        "appid": "fceeaac1-8f96-46d6-9c3b-896e363eb004",
        "identifier": "test_connectivity",
        "parameters": [{}]
    }

    # Execute Action
    action_result_str = connector._handle_action(json.dumps(in_json), None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["message"] == "Active connection"


def test_block_vcr(cassette, connector: Soar_Null_RouterConnector):
    cidr = '151.45.29.79/32'
    in_json = {
        "appid": "fceeaac1-8f96-46d6-9c3b-896e363eb004",
        "identifier": "block",
        "parameters": [{
            "cidr": cidr,
            "source": 'TEST',
            "why": "Malicious IP!",
            "duration": '100',
        }]
    }

    # Execute Action
    dump = json.dumps(in_json)
    action_result_str = connector._handle_action(dump, None)
    action_result = json.loads(action_result_str)

    # Assertion
    assert action_result[0]["message"] == f"Blocked {cidr}"
