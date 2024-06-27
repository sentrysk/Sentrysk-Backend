#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import Document,StringField, DateTimeField, ReferenceField
from datetime import datetime

from Users.models import User
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
    created_by = ReferenceField(User)

    def serialize(self):
        return {
            "id":str(self.id),
            "type":self.type,
            "token":self.token,
            "created":self.created,
            "created_by": self.created_by.safe_serialize()
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################
