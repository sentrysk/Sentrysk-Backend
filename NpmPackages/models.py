#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    EmbeddedDocument, StringField
)
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
##############################################################################