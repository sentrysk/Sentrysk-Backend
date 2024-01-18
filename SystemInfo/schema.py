#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# Schemas
##############################################################################
class RegisterSchema(Schema):
    os                  = fields.Raw(required=True)
    domain              = fields.Raw(required=True)
    cpu                 = fields.Raw(required=True)
    memory              = fields.Raw(required=True)
    disks               = fields.Raw(required=True)
    network_interfaces  = fields.Raw(required=True)

class UpdateSchema(Schema):
    os                  = fields.Raw()
    domain              = fields.Raw()
    cpu                 = fields.Raw()
    memory              = fields.Raw()
    disks               = fields.Raw()
    network_interfaces  = fields.Raw()
##############################################################################