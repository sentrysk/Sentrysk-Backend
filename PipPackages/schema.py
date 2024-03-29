#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# PipPackage Schema
##############################################################################
class PipPackageSchema(Schema):
    name         = fields.Str(required=True)
    version      = fields.Str(required=True)
##############################################################################

# Register Schema
##############################################################################
class RegisterSchema(Schema):
    is_installed = fields.Boolean(required=True)
    pip_packages = fields.List(fields.Nested(PipPackageSchema))
##############################################################################