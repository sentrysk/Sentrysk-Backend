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

'''
Current Config Style
{
    "api": {
      "base_url": "http://localhost:8000",
      "endpoints": {
        "system_info": "/sysinfo/",
        "user_info": "/sysusers/",
        "installed_programs": "/sysapps/",
        "service_info": "/sysservices/",
        "last_logons": "/sysusers/lastlogons/",
        "pip_pkgs": "/pippkgs/",
        "npm_pkgs": "/npmpkgs/",
        "docker_info": "/dockerinfo/"
      },
      "agent_token": "your_agent_token_here"
    },
    "dirs": {
      "home_dir": "/path/to/home/directory",
      "logfile": "logs/agent_logs.log"
    },
    "scheduled_jobs":{
      "send_system_info":{"time": "00:00"},
      "send_user_info":{"interval": 1, "unit": "minutes"},
      "send_installed_programs": {"interval": 1, "unit": "minutes"},
      "send_service_info": {"interval": 1, "unit": "minutes"},
      "send_last_logons": {"interval": 1, "unit": "minutes"},
      "send_pip_packages": {"interval": 1, "unit": "minutes"},
      "send_npm_packages": {"interval": 1, "unit": "minutes"},
      "send_docker_info": {"interval": 1, "unit": "minutes"}
    }
}
'''

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

    def serialize(self):
        return {
            "agent": self.agent,
            "api": self.api,
            "dirs": self.dirs,
            "scheduled_jobs": self.scheduled_jobs,
            "updated": self.updated
        }

    def __str__(self):
        return str(self.serialize())

class ChangeLogAgentConfig(Document):
    agent_config    = ReferenceField(AgentConfig)
    timestamp       = DateTimeField(default=datetime.utcnow)
    changes         = DictField()

    def serialize(self):
        return {
            "id":str(self.id),
            "timestamp":self.timestamp,
            "changes":self.changes
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################
