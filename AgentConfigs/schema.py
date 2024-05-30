#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields, validate
from enum import Enum,unique
##############################################################################

# Global Values
##############################################################################
MAX_LEN = 50
##############################################################################

# Regexs
##############################################################################
# Regular expressions optimized to prevent catastrophic backtracking
VALID_PATH_REGEX    = r'^/[a-zA-Z0-9_/]+/$'
VALID_DIR_REGEX     = r'^/[a-zA-Z0-9_/]+$'
VALID_LOGFILE_REGEX = r'^[a-zA-Z0-9_/]+\.log$'
VALID_TIME_REGEX    = r'^\d{2}:\d{2}$'
##############################################################################

# Enums
##############################################################################
@unique
class UnitEnum(str,Enum):
    minutes   : str = "minutes"
    hours     : str = "hours"
##############################################################################

# Schemas
##############################################################################
from marshmallow import Schema, fields, validate

class EndpointsSchema(Schema):
    system_info         = fields.String(
        required=True, validate=[validate.Length(max=MAX_LEN), validate.Regexp(VALID_PATH_REGEX)]
    )
    user_info           = fields.String(
        required=True, validate=[validate.Length(max=MAX_LEN), validate.Regexp(VALID_PATH_REGEX)]
    )
    installed_programs  = fields.String(
        required=True, validate=[validate.Length(max=MAX_LEN), validate.Regexp(VALID_PATH_REGEX)]
    )
    service_info        = fields.String(
        required=True, validate=[validate.Length(max=MAX_LEN), validate.Regexp(VALID_PATH_REGEX)]
    )
    last_logons         = fields.String(
        required=True, validate=[validate.Length(max=MAX_LEN), validate.Regexp(VALID_PATH_REGEX)]
    )
    pip_pkgs            = fields.String(
        required=True, validate=[validate.Length(max=MAX_LEN), validate.Regexp(VALID_PATH_REGEX)]
    )
    npm_pkgs            = fields.String(
        required=True, validate=[validate.Length(max=MAX_LEN), validate.Regexp(VALID_PATH_REGEX)]
    )
    docker_info         = fields.String(
        required=True, validate=[validate.Length(max=MAX_LEN), validate.Regexp(VALID_PATH_REGEX)]
    )

class ApiSchema(Schema):
    base_url = fields.String(required=True, validate=validate.URL())
    endpoints = fields.Nested(EndpointsSchema, required=True)
    agent_token = fields.String(required=True)

class DirsSchema(Schema):
    home_dir = fields.String(required=True)
    logfile = fields.String(required=True)

class ScheduledJobSchema(Schema):
    time = fields.String(required=False)
    interval = fields.Integer(required=False)
    unit = fields.String(required=False, validate=validate.OneOf([val for val in UnitEnum]))

class ScheduledJobsSchema(Schema):
    send_system_info = fields.Nested(ScheduledJobSchema, required=True)
    send_user_info = fields.Nested(ScheduledJobSchema, required=True)
    send_installed_programs = fields.Nested(ScheduledJobSchema, required=True)
    send_service_info = fields.Nested(ScheduledJobSchema, required=True)
    send_last_logons = fields.Nested(ScheduledJobSchema, required=True)
    send_pip_packages = fields.Nested(ScheduledJobSchema, required=True)
    send_npm_packages = fields.Nested(ScheduledJobSchema, required=True)
    send_docker_info = fields.Nested(ScheduledJobSchema, required=True)

class AgentConfigRegisterSchema(Schema):
    api = fields.Nested(ApiSchema, required=True)
    dirs = fields.Nested(DirsSchema, required=True)
    scheduled_jobs = fields.Nested(ScheduledJobsSchema, required=True)

##############################################################################