#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import Schema, fields, validate
from enum import Enum,unique
##############################################################################

# Regexs
##############################################################################

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
    system_info = fields.String(required=True)
    user_info = fields.String(required=True)
    installed_programs = fields.String(required=True)
    service_info = fields.String(required=True)
    last_logons = fields.String(required=True)
    pip_pkgs = fields.String(required=True)
    npm_pkgs = fields.String(required=True)
    docker_info = fields.String(required=True)

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