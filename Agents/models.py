#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import Document,StringField, DateTimeField
from datetime import datetime
##############################################################################

# Configs
##############################################################################

##############################################################################


# Models
##############################################################################
class Agent(Document):
    type    = StringField(required=True) # Agent type E.g Linux, Windows
    token   = StringField(required=True, unique=True)
    created = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        return {
            "id":str(self.id),
            "type":self.type,
            "token":self.token,
            "created":self.created
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################
