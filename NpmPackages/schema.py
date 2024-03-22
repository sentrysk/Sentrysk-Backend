#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# NpmPackage Schema
##############################################################################
class NpmPackageSchema(Schema):
    name         = fields.Str(required=True)
    version      = fields.Str(required=True)
##############################################################################

# Register Schema
##############################################################################
class RegisterSchema(Schema):
    is_installed = fields.Boolean(required=True)
    npm_packages = fields.List(fields.Nested(NpmPackageSchema))
##############################################################################