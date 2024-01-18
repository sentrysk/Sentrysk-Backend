#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# Service Schema
##############################################################################
class SysUserSchema(Schema):
    username        = fields.Str(required=True)
    user_id         = fields.Str()
    group_id        = fields.Str()
    home_directory  = fields.Str()
    shell           = fields.Str()
    full_name       = fields.Str()
    comment         = fields.Str()
    flags           = fields.List(fields.Str())
    sid             = fields.Str()
##############################################################################

# Register Schema
##############################################################################
class RegisterSchema(Schema):
    users = fields.List(fields.Nested(SysUserSchema))
##############################################################################