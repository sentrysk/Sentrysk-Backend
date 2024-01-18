#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, ReferenceField, DateTimeField, ListField,
    EmbeddedDocument, EmbeddedDocumentField, StringField
)
from Agents.models import Agent
from datetime import datetime
##############################################################################

# LogonData Model
##############################################################################
class LogonData(EmbeddedDocument):
    username        = StringField()
    last_logon      = DateTimeField()

    def serialize(self):
        data = {
            "username": self.username,
            "last_logon": self.last_logon
        }
        return data

    def __str__(self):
        return str(self.serialize())
##############################################################################

# SystemLastLogons Model
##############################################################################
class SystemLastLogons(Document):
    agent               = ReferenceField(Agent)
    last_logons         = ListField(EmbeddedDocumentField(LogonData))
    updated             = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        # Serialize All LogonData
        serialized_logons = []
        for logon in self.last_logons:
            serialized_logons.append(logon.serialize())
        
        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "last_logons":serialized_logons,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################