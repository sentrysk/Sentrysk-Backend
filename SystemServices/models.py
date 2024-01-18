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

# Global Values
##############################################################################
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
##############################################################################

##############################################################################
class Service(EmbeddedDocument):
    display_name    = StringField()
    service_name    = StringField()
    status          = StringField()
    description     = StringField()

    def __eq__(self, other):
        return (
            self.display_name == other.display_name and
            self.service_name == other.service_name and
            self.status == other.status and
            self.description == other.description
        )

    def serialize(self):
        data = {
            "display_name": self.display_name,
            "service_name": self.service_name,
            "status": self.status,
            "description": self.description
        }

        return data

    def __str__(self):
        return str(self.serialize())

class SystemServices(Document):
    agent     = ReferenceField(Agent)
    services  = ListField(EmbeddedDocumentField(Service))
    updated   = DateTimeField(default=datetime.utcnow)

    # Compare 2 Service Data
    def compare_servies(self, other):
        if not isinstance(other, SystemServices):
            raise ValueError("Comparison should be done with another SystemServices instance")

        self_services = {service.service_name: service for service in self.services}
        other_services = {service.service_name: service for service in other.services}

        # Newly Added Services
        new_services = [service.serialize() for service_name, service in other_services.items() if service_name not in self_services]
        # Deleted Services
        deleted_services = [service.serialize() for service_name, service in self_services.items() if service_name not in other_services]
        # Updated Services and Fields
        updated_services = {}

        # Find the Updated Fields
        for service_name in self_services:
            if service_name in other_services and self_services[service_name] != other_services[service_name]:
                updated_fields = {}
                for field in Service._fields:
                    if str(self_services[service_name][field]) != str(other_services[service_name][field]):
                        updated_fields[field] = {
                            "previous_value":self_services[service_name][field],
                            "new_value":other_services[service_name][field]
                        }
                # Add Updated Fields to Updated services Dict
                updated_services[service_name] = updated_fields

        # Return Compared Data
        return new_services, deleted_services, updated_services
    
    def serialize(self):
        # Serialize All Services
        serialized_services = []
        for service in self.services:
            serialized_services.append(service.serialize())

        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "services":serialized_services,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())

class ChangeLogSystemServices(Document):
    services   = ReferenceField(SystemServices)
    timestamp  = DateTimeField(default=datetime.utcnow)
    changes    = DictField()

    def serialize(self):
        return {
            "id":str(self.id),
            "timestamp":self.timestamp,
            "changes":self.changes
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################