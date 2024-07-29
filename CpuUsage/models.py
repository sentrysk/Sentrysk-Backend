#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, ReferenceField, DateTimeField, FloatField
)
from datetime import datetime

from Agents.models import Agent
##############################################################################


# Models
##############################################################################
class CpuUsage(Document):
    agent           = ReferenceField(Agent)
    timestamp       = DateTimeField(required=True,default=datetime.utcnow)
    cpu_usage       = FloatField(required=True)

    meta = {
        'indexes': ['timestamp']
    }

    # Helper function to serialize CpuUsage objects
    def serialize(self):
        return {
            'agent': str(self.agent.id),
            'timestamp': self.timestamp,
            'cpu_usage': self.used_size,
        }
    
    def __str__(self):
        return str(self.serialize())
##############################################################################