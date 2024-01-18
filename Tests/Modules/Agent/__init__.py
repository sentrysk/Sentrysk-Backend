#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import json
import random

from Modules.Config import Urls,Endpoints
##############################################################################


# Config
##############################################################################
AGENT_REG_URL = Urls.base_url + Endpoints.agents_reg_ep
AGENT_UPDT_URL = Urls.base_url + Endpoints.agents_ep 
##############################################################################


# Global Values
##############################################################################
VALID_AGENT_TYPES = [
    'windows',
    'linux',
    'macos'
]
##############################################################################


# Test Agent Register Success
##############################################################################
def test_register_agent_success(token):    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    reg_data = {
        'type': random.choice(VALID_AGENT_TYPES)
    }

    response = requests.request(
        "POST",
        AGENT_REG_URL,
        data=json.dumps(reg_data),
        headers=headers
    )

    assert "Agent registered successfully." in response.text
    assert response.status_code == 201

    return response.json()["agent"]
##############################################################################

# Test Agent Register Wrong Agent Type
##############################################################################
def test_register_wrong_agent_types(token):
    agent_types = [
        'WinDowS',
        'LiNuX',
        'MaCos',
        '',
        'Test',
        'Test Space'
    ]
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    for agent_type in agent_types:
        reg_data = {
            'type': agent_type
        }

        response = requests.request(
            "POST",
            AGENT_REG_URL,
            data=json.dumps(reg_data),
            headers=headers
        )

        assert response.status_code == 400

    return True
##############################################################################

# Test Agent Register Double Agent Type
##############################################################################
def test_register_double_agent_type(token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    reg_data = {
        'type': 'Test',
        'type': 'Test2'
    }

    response = requests.request(
        "POST",
        AGENT_REG_URL,
        data=json.dumps(reg_data),
        headers=headers
    )

    assert response.status_code == 400

    return True
##############################################################################

# Test Update Wrong Agent ID
##############################################################################
def test_update_wrong_agent_id(token):
    test_agent_ids = [
        "abc123",
        "123",
        " ",
        "@",
        "%27OR%201%3D1--", # 'OR 1=1--
        "%24where%20%3A%20%271%20%3D%3D%201" # $where : '1 == 1
    ]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    update_data = {
        'type': random.choice(VALID_AGENT_TYPES)
    }

    for test_agent_id in test_agent_ids:
        response = requests.request(
            "PUT",
            AGENT_UPDT_URL + "/" +  test_agent_id,
            data=json.dumps(update_data),
            headers=headers
        )

        assert response.status_code == 400

    return True
##############################################################################

# Test Successfully Update Agent Type
##############################################################################
def test_successfully_update_agent_type(agent_id,token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    update_data = {
        'type': random.choice(VALID_AGENT_TYPES)
    }

    response = requests.request(
        "PUT",
        AGENT_UPDT_URL + "/" +  agent_id,
        data=json.dumps(update_data),
        headers=headers
    )

    assert response.status_code == 200

    return True
##############################################################################