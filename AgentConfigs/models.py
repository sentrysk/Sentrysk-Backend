#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, DictField, ReferenceField, DateTimeField, ListField,
    EmbeddedDocument, EmbeddedDocumentField, StringField, IntField
)
from Agents.models import Agent
from datetime import datetime
##############################################################################


# Models
##############################################################################
class Endpoints(EmbeddedDocument):
    system_info        = StringField(required=True)
    user_info          = StringField(required=True)
    installed_programs = StringField(required=True)
    service_info       = StringField(required=True)
    last_logons        = StringField(required=True)
    pip_pkgs           = StringField(required=True)
    npm_pkgs           = StringField(required=True)
    docker_info        = StringField(required=True)

class Api(EmbeddedDocument):
    base_url    = StringField(required=True)
    endpoints   = EmbeddedDocumentField(Endpoints, required=True)
    agent_token = StringField(required=True)

class Dirs(EmbeddedDocument):
    home_dir = StringField(required=True)
    logfile  = StringField(required=True)

class ScheduledJob(EmbeddedDocument):
    time     = StringField()
    interval = IntField()
    unit     = StringField()

class ScheduledJobs(EmbeddedDocument):
    send_system_info        = EmbeddedDocumentField(ScheduledJob, required=True)
    send_user_info          = EmbeddedDocumentField(ScheduledJob, required=True)
    send_installed_programs = EmbeddedDocumentField(ScheduledJob, required=True)
    send_service_info       = EmbeddedDocumentField(ScheduledJob, required=True)
    send_last_logons        = EmbeddedDocumentField(ScheduledJob, required=True)
    send_pip_packages       = EmbeddedDocumentField(ScheduledJob, required=True)
    send_npm_packages       = EmbeddedDocumentField(ScheduledJob, required=True)
    send_docker_info        = EmbeddedDocumentField(ScheduledJob, required=True)

class AgentConfig(Document):
    agent          = ReferenceField(Agent)
    api            = EmbeddedDocumentField(Api, required=True)
    dirs           = EmbeddedDocumentField(Dirs, required=True)
    scheduled_jobs = EmbeddedDocumentField(ScheduledJobs, required=True)
    updated        = DateTimeField(default=datetime.utcnow)
##############################################################################
