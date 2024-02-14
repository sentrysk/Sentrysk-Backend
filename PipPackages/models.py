#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, DictField, ReferenceField, DateTimeField, ListField,
    EmbeddedDocument, EmbeddedDocumentField, StringField
)
from Agents.models import Agent
from datetime import datetime
##############################################################################


# Models
##############################################################################
class PipPackage(EmbeddedDocument):
    name            = StringField()
    version         = StringField()

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.version == other.version
        )

    def serialize(self):
        data = {
            "name": self.name,
            "version": self.version
        }
        return data

    def __str__(self):
        return str(self.serialize())

class InstalledPipPackages(Document):
    agent           = ReferenceField(Agent)
    pip_packages    = ListField(EmbeddedDocumentField(PipPackage))
    updated         = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        # Serialize All PipPackages
        serialized_pip_packages = []
        for pip_pkg in self.pip_packages:
            serialized_pip_packages.append(pip_pkg.serialize())
        
        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "pip_packages":serialized_pip_packages,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())

class ChangeLogInstalledPipPackages(Document):
    pip_packages    = ReferenceField(InstalledPipPackages)
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