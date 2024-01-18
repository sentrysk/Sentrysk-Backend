#!/usr/bin/env python3

# Libraries
##############################################################################
import requests
import json
from faker import Faker

from Modules.Config import Urls,Endpoints
##############################################################################


# Config
##############################################################################
fake = Faker()

REG_URL = Urls.base_url + Endpoints.register_ep
##############################################################################


# Generate User Data
##############################################################################
def generate_user_data():
    user_data = {}
    user_data["name"] = str(fake.unique.first_name())
    user_data["lastname"] = str(fake.unique.first_name())
    user_data["email"] =user_data["name"].lower()\
        +"."+user_data["lastname"].lower()\
        +"@"+str(fake.free_email_domain())
    user_data["password"] = "1234"
    
    return user_data
##############################################################################

# Test Successfully Registration
##############################################################################
def test_register_success():
    user_data = generate_user_data()

    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request(
        "POST",
        REG_URL,
        data=json.dumps(user_data),
        headers=headers
    )

    assert "User registered successfully." in response.text
    assert response.status_code == 201
    
    return user_data
##############################################################################

# Test Invalid Names
##############################################################################
def test_register_invalid_name():
    testing_user_data = [
        123423,
        "!'.abcc-",
        "'ab123asdf",
        "||",
        "space  test   third",
        "",
        "space test third"
    ]

    headers = {
        'Content-Type': 'application/json'
    }
    
    for t_data in testing_user_data:
        user_data = generate_user_data()
        user_data["name"] = t_data

        response = requests.request(
            "POST",
            REG_URL,
            data=json.dumps(user_data),
            headers=headers
        )

        assert "error" in response.text
        assert response.status_code == 400
    
    return True
##############################################################################

# Test Invalid Lastnames
##############################################################################
def test_register_invalid_lastname():
    testing_user_data = [
        123423,
        "!'.abcc-",
        "'ab123asdf",
        "||",
        "space  test",
        "",
        "space test"
    ]

    headers = {
        'Content-Type': 'application/json'
    }
    
    for t_data in testing_user_data:
        user_data = generate_user_data()
        user_data["lastname"] = t_data

        response = requests.request(
            "POST",
            REG_URL,
            data=json.dumps(user_data),
            headers=headers
        )

        assert "error" in response.text
        assert response.status_code == 400
    
    return True
##############################################################################

# Test Invalid Email
##############################################################################
def test_register_invalid_email():
    testing_user_data = [
        123423,
        "!'.abcc-",
        "'ab123asdf",
        "||",
        "",
        "space @test.com",
        "a@@.com",
        "@",
        "@.ta",
        "1@1...",
        "tes__@.com"
    ]

    headers = {
        'Content-Type': 'application/json'
    }
    
    for t_data in testing_user_data:
        user_data = generate_user_data()
        user_data["email"] = t_data

        response = requests.request(
            "POST",
            REG_URL,
            data=json.dumps(user_data),
            headers=headers
        )

        assert "error" in response.text
        assert response.status_code == 400
    
    return True
##############################################################################
