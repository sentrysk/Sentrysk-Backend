#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# Service Schema
##############################################################################
class ServiceSchema(Schema):
    display_name    = fields.Str(required=True)
    service_name    = fields.Str(required=True)
    status          = fields.Str(required=True)
    description     = fields.Str(required=False)
##############################################################################

# Register Schema
##############################################################################
class RegisterSchema(Schema):
    services = fields.List(fields.Nested(ServiceSchema))
##############################################################################