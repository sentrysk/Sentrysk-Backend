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
class Images(EmbeddedDocument):
    image_id        = StringField()
    tags            = StringField()
    size            = StringField()
    created         = DateTimeField()
    labels          = StringField()

    def serialize(self):
        data = {
            "image_id": self.image_id,
            "tags": self.tags,
            "size": self.size,
            "created": self.created,
            "labels": self.labels
        }
        return data

    def __str__(self):
        return str(self.serialize())
    
class Containers(EmbeddedDocument):
    container_id     = StringField()
    image            = StringField()
    status           = StringField()
    ports            = StringField()
    networks         = StringField()
    created          = DateTimeField()
    labels           = StringField()

    def serialize(self):
        data = {
            "container_id": self.container_id,
            "image": self.image,
            "status": self.status,
            "ports": self.ports,
            "networks": self.networks,
            "created": self.created,
            "labels": self.labels
        }
        return data

    def __str__(self):
        return str(self.serialize())
    
class Volumes(EmbeddedDocument):
    volume_name      = StringField()
    mountpoint       = StringField()
    created          = DateTimeField()
    labels           = StringField()

    def serialize(self):
        data = {
            "volume_name": self.volume_name,
            "mountpoint": self.mountpoint,
            "created": self.created,
            "labels": self.labels
        }
        return data

    def __str__(self):
        return str(self.serialize())
    
class Networks(EmbeddedDocument):
    network_id       = StringField()
    name             = StringField()
    driver           = StringField()
    created          = DateTimeField()
    labels           = StringField()

    def serialize(self):
        data = {
            "network_id": self.network_id,
            "name": self.name,
            "driver": self.driver,
            "created": self.created,
            "labels": self.labels
        }
        return data

    def __str__(self):
        return str(self.serialize())