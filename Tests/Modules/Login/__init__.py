#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import json

from Modules.Config import Urls,Endpoints
##############################################################################


# Config
##############################################################################
LOGIN_URL = Urls.base_url + Endpoints.login_ep
##############################################################################


# Test Login Success
##############################################################################
def test_login_success(user_data):
    headers = {
        'Content-Type': 'application/json'
    }

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    response = requests.request(
        "POST",
        LOGIN_URL,
        data=json.dumps(login_data),
        headers=headers
    )

    assert "Login successful." in response.text

    return response.json()["token"]
##############################################################################


# Test Login Invalid Email
##############################################################################
def test_login_invalid_email():
    invalid_emails = [
        "space @test.com",
        "",
        " ",
        "a@@.com",
        "@",
        "@.ta",
        "1@1...",
        "tes__@.com"
    ]

    headers = {
        'Content-Type': 'application/json'
    }
    
    for t_email in invalid_emails:
        login_data = {
            "email": t_email,
            "password": "1234"
        }

        response = requests.request(
            "POST",
            LOGIN_URL,
            data=json.dumps(login_data),
            headers=headers
        )

        assert "Not a valid email address." in response.text
        assert response.status_code == 400

    return True
##############################################################################