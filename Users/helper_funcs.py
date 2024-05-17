#!/usr/bin/env python3

# Libraries
##############################################################################
import jwt
from Shared.configs import SECRET_KEY,JWT_ALG
from flask import jsonify
##############################################################################

# Functions
##############################################################################
def get_email_by_token(jwtToken):
    try:
        tokenValue = jwt.decode(
            jwtToken,
            SECRET_KEY,
            algorithms=[JWT_ALG]
        )
        return tokenValue["email"]
    except Exception as e:
        return jsonify(
            {
                'message':'Token is invalid'
            }
        ),498
##############################################################################