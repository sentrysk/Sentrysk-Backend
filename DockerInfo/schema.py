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
    
# Containers Schema
##############################################################################
class ContainersSchema(Schema):
    container_id = fields.Str(required=True)
    image        = fields.Str(required=True)
    status       = fields.Str(required=True)
    ports        = fields.Str(required=False)
    networks     = fields.Str(required=False)
    created      = fields.DateTime(required=True)
    labes        = fields.Str(required=False)
##############################################################################

# Register Schema
##############################################################################
class RegisterSchema(Schema):
    is_installed    = fields.Boolean(required=True)
    images          = fields.List(fields.Nested(ImagesSchema))
    containers      = fields.List(fields.Nested(ContainersSchema))
##############################################################################