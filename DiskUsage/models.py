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

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    # Helper function to serialize DiskUsage objects
    def serialize(self):
        return {
            'agent': str(self.agent.id),
            'timestamp': self.timestamp,
            'device': self.device,
            'total_size': self.convert_size(self.total_size),
            'used_size': self.convert_size(self.used_size),
            'free_size': self.convert_size(self.free_size),
            'percent': self.percent
        }
    
    def __str__(self):
        return str(self.serialize())
##############################################################################