#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# App Schema
##############################################################################
class AppSchema(Schema):
    name         = fields.Str(required=True)
    version      = fields.Str(required=False)
    installed_by = fields.Str(required=False)
##############################################################################

# Register Schema
##############################################################################
class RegisterSchema(Schema):
    apps = fields.List(fields.Nested(AppSchema))
##############################################################################