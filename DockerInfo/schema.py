#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields
##############################################################################

# Images Schema
##############################################################################
class ImagesSchema(Schema):
    image_id     = fields.Str(required=True)
    tags         = fields.List(fields.Str(),required=True)
    size         = fields.Str(required=True)
    created      = fields.DateTime(required=True)
    labels       = fields.Dict(required=True,allow_none=True)
##############################################################################
    
# Containers Schema
##############################################################################
class ContainersSchema(Schema):
    container_id = fields.Str(required=True)
    image        = fields.Str(required=True)
    status       = fields.Str(required=True)
    ports        = fields.Dict(required=True)
    networks     = fields.Dict(required=True)
    created      = fields.DateTime(required=True)
    labels       = fields.Dict(required=True,allow_none=True)
##############################################################################
    
# Volumes Schema
##############################################################################
class VolumesSchema(Schema):
    volume_name  = fields.Str(required=True)
    mountpoint   = fields.Str(required=True)
    created      = fields.DateTime(required=True)
    labels       = fields.Dict(required=True,allow_none=True)
##############################################################################
    
# Networks Schema
##############################################################################
class NetworksSchema(Schema):
    network_id   = fields.Str(required=True)
    name         = fields.Str(required=True)
    driver       = fields.Str(required=True)
    created      = fields.DateTime(required=True)
    labels       = fields.Dict(required=True,allow_none=True)
##############################################################################

# Register Schema
##############################################################################
class RegisterSchema(Schema):
    is_installed    = fields.Boolean(required=True)
    images          = fields.List(fields.Nested(ImagesSchema))
    containers      = fields.List(fields.Nested(ContainersSchema))
    volumes         = fields.List(fields.Nested(VolumesSchema))
    networks        = fields.List(fields.Nested(NetworksSchema))
    disk_usage      = fields.Str(required=True)
##############################################################################