#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields, validate
##############################################################################

# Regexs
##############################################################################
NAME_REGX = r'^[\w]{2,30}(?: [\w]{1,30})?$'
LNAME_REGX = r'^[\w]{2,30}$'
##############################################################################

# Schemas
##############################################################################
class RegisterSchema(Schema):
    name       = fields.Str(required = True,validate=validate.Regexp(NAME_REGX))
    lastname   = fields.Str(required = True,validate=validate.Regexp(LNAME_REGX))
    email      = fields.Email(required = True)
    password   = fields.Str(required = True)

class LoginSchema(Schema):
    email      = fields.Email(required = True)
    password   = fields.Str(required = True)
##############################################################################