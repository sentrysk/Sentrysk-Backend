#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# Images Schema
##############################################################################
class ImagesSchema(Schema):
    image_id     = fields.Str(required=True)
    tags         = fields.Str(required=False)
    size         = fields.Str(required=True)
    created      = fields.DateTime(required=True)
    labes        = fields.Str(required=False)
##############################################################################

# Register Schema
##############################################################################
class RegisterSchema(Schema):
    is_installed    = fields.Boolean(required=True)
    images          = fields.List(fields.Nested(ImagesSchema))
##############################################################################