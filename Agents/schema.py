#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields, validate
from enum import Enum,unique
##############################################################################

# Regexs
##############################################################################
ID_REGX = r'^[a-fA-F0-9]{24}$'
##############################################################################

# Enums
##############################################################################
@unique
class AgentTypeEnum(str,Enum):
    windows   : str = "windows"
    linux     : str = "linux"
    macos     : str = "macos"
##############################################################################

# Schemas
##############################################################################
class AgentTypeSchema(Schema):
    type = fields.Str(
        required=True, 
        validate = validate.OneOf([val for val in AgentTypeEnum])
    )

class UpdateSchema(Schema):
    agent_id = fields.Str(
        validate=validate.Regexp(ID_REGX)
    )
    type = fields.Str(
        required=True, 
        validate = validate.OneOf([val for val in AgentTypeEnum])
    )
    token = fields.UUID()
##############################################################################