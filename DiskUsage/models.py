#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, ReferenceField, StringField, DateTimeField, FloatField
)

from Agents.models import Agent

from datetime import datetime
import math
##############################################################################

# Configs
##############################################################################

##############################################################################


# Models
##############################################################################
class DiskUsage(Document):
    agent           = ReferenceField(Agent)
    timestamp       = DateTimeField(required=True,default=datetime.utcnow)
    device          = StringField(required=True)
    total_size      = FloatField(required=True)
    used_size       = FloatField(required=True)
    free_size       = FloatField(required=True)
    percent         = FloatField(required=True)

    meta = {
        'indexes': ['timestamp']
    }


    # Helper function to serialize DiskUsage objects
    def serialize(self):
        return {
            'agent': str(self.agent.id),
            'timestamp': self.timestamp.isoformat(),
            'device': self.device,
            'total_size': self.convert_size(self.total_size),
            'used_size': self.convert_size(self.used_size),
            'free_size': self.convert_size(self.free_size),
            'percent': self.percent
        }
    
    def __str__(self):
        return str(self.serialize())
##############################################################################