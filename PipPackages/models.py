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
    is_installed    = BooleanField()
    pip_packages    = ListField(EmbeddedDocumentField(PipPackage))
    updated         = DateTimeField(default=datetime.utcnow)

    # To compare 2 Pip Package Data
    def compare_pip_pkgs(self, other):
        if not isinstance(other, InstalledPipPackages):
            raise ValueError("Comparison should be done with another InstalledPipPackages instance")

        self_pip_pkgs = {pip_pkg.name: pip_pkg for pip_pkg in self.pip_pkgs}
        other_pip_pkgs = {pip_pkg.name: pip_pkg for pip_pkg in other.pip_pkgs}

        # Newly Added pip_pkgs
        new_pip_pkgs = [pip_pkg.serialize() for name, pip_pkg in other_pip_pkgs.items() if name not in self_pip_pkgs]
        # Deleted pip_pkgs
        deleted_pip_pkgs = [pip_pkg.serialize() for name, pip_pkg in self_pip_pkgs.items() if name not in other_pip_pkgs]
        # Updated pip_pkgs and Fields
        updated_pip_pkgs = {}

        # Find the Updated Fields
        for pkg_name in self_pip_pkgs:
            if pkg_name in other_pip_pkgs and self_pip_pkgs[pkg_name] != other_pip_pkgs[pkg_name]:
                updated_fields = {}
                for field in PipPackage._fields:
                    if str(self_pip_pkgs[pkg_name][field]) != str(other_pip_pkgs[pkg_name][field]):
                        updated_fields[field] = {
                            "previous_value":self_pip_pkgs[pkg_name][field],
                            "new_value":other_pip_pkgs[pkg_name][field]
                        }
                # Add Updated Fields to Updated pip_pkgs Dict
                updated_pip_pkgs[pkg_name] = updated_fields

        # Return Compared Data
        return new_pip_pkgs, deleted_pip_pkgs, updated_pip_pkgs

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