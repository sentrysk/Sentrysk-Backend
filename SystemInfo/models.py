#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, DictField, ReferenceField,  DateTimeField
)
from Agents.models import Agent
from datetime import datetime
##############################################################################

##############################################################################
class SystemInfo(Document):
    agent               = ReferenceField(Agent)
    os                  = DictField()
    domain              = DictField()
    cpu                 = DictField()
    memory              = DictField()
    disks               = DictField()
    network_interfaces  = DictField()
    updated             = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "os":self.os,
            "domain":self.domain,
            "cpu":self.cpu,
            "memory":self.memory,
            "disks":self.disks,
            "network_interfaces":self.network_interfaces,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())

class ChangeLogSystemInfo(Document):
    system_info     = ReferenceField(SystemInfo)
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