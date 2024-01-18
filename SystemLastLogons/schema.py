#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# Login Schema
##############################################################################
class LoginSchema(Schema):
    username    = fields.Str(required=True)
    last_logon  = fields.DateTime(required=True)
##############################################################################

# Last Logons Schema
##############################################################################
class LastLogonSchema(Schema):
    last_logons = fields.List(fields.Nested(LoginSchema))
##############################################################################