#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, StringField, DateTimeField, FloatField
)

from Agents.models import Agent
from datetime import datetime
##############################################################################

# Configs
##############################################################################

##############################################################################


# Models
##############################################################################
class DiskUsage(Document):
    timestamp       = DateTimeField(required=True,default=datetime.utcnow)
    device          = StringField(required=True)
    total           = FloatField(required=True)
    used            = FloatField(required=True)
    free            = FloatField(required=True)
    percent         = FloatField(required=True)

    meta = {
        'indexes': ['timestamp']
    }

##############################################################################