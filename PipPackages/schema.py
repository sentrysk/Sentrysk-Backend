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
    pip_packages = fields.List(fields.Nested(PipPackageSchema))
##############################################################################