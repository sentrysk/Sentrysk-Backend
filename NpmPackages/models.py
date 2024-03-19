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

    # To compare 2 Npm Package Data
    def compare_npm_pkgs(self, other):
        if not isinstance(other, InstalledNpmPackages):
            raise ValueError("Comparison should be done with another InstalledNpmPackages instance")

        self_npm_pkgs = {npm_pkg.name: npm_pkg for npm_pkg in self.npm_packages}
        other_npm_pkgs = {npm_pkg.name: npm_pkg for npm_pkg in other.npm_packages}

        # Newly Added npm_pkgs
        new_npm_pkgs = [npm_pkg.serialize() for name, npm_pkg in other_npm_pkgs.items() if name not in self_npm_pkgs]
        # Deleted npm_pkgs
        deleted_npm_pkgs = [npm_pkg.serialize() for name, npm_pkg in self_npm_pkgs.items() if name not in other_npm_pkgs]
        # Updated npm_pkgs and Fields
        updated_npm_pkgs = {}

        # Find the Updated Fields
        for pkg_name in self_npm_pkgs:
            if pkg_name in other_npm_pkgs and self_npm_pkgs[pkg_name] != other_npm_pkgs[pkg_name]:
                updated_fields = {}
                for field in NpmPackage._fields:
                    if str(self_npm_pkgs[pkg_name][field]) != str(other_npm_pkgs[pkg_name][field]):
                        updated_fields[field] = {
                            "previous_value":self_npm_pkgs[pkg_name][field],
                            "new_value":other_npm_pkgs[pkg_name][field]
                        }
                # Add Updated Fields to Updated npm_pkgs Dict
                updated_npm_pkgs[pkg_name] = updated_fields

        # Return Compared Data
        return new_npm_pkgs, deleted_npm_pkgs, updated_npm_pkgs

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