#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, DictField, ReferenceField, DateTimeField, ListField,
    EmbeddedDocument, EmbeddedDocumentField, StringField, BooleanField
)
from Agents.models import Agent
from datetime import datetime
##############################################################################


# Models
##############################################################################
class NpmPackage(EmbeddedDocument):
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
    
class InstalledNpmPackages(Document):
    agent           = ReferenceField(Agent)
    is_installed    = BooleanField()
    npm_packages    = ListField(EmbeddedDocumentField(NpmPackage))
    updated         = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        # Serialize All NpmPackages
        serialized_npm_packages = []
        for npm_pkg in self.npm_packages:
            serialized_npm_packages.append(npm_pkg.serialize())
        
        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "is_installed": self.is_installed,
            "npm_packages":serialized_npm_packages,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################