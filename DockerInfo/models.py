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

# Docker Images Model
class Images(EmbeddedDocument):
    image_id        = StringField()
    tags            = ListField()
    size            = StringField()
    created         = DateTimeField()
    labels          = DictField()

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

# Docker Containers Model
class Containers(EmbeddedDocument):
    container_id     = StringField()
    image            = StringField()
    status           = StringField()
    ports            = DictField()
    networks         = DictField()
    created          = DateTimeField()
    labels           = DictField()

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

# Docker Volumes Model 
class Volumes(EmbeddedDocument):
    volume_name      = StringField()
    mountpoint       = StringField()
    created          = DateTimeField()
    labels           = DictField()

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

# Docker Networks Model
class Networks(EmbeddedDocument):
    network_id       = StringField()
    name             = StringField()
    driver           = StringField()
    created          = DateTimeField()
    labels           = DictField()

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
    
# Docker Info Model
class DockerInfo(Document):
    agent           = ReferenceField(Agent)
    is_installed    = BooleanField()
    images          = ListField(EmbeddedDocumentField(Images))
    containers      = ListField(EmbeddedDocumentField(Containers))
    volumes         = ListField(EmbeddedDocumentField(Volumes))
    networks        = ListField(EmbeddedDocumentField(Networks))
    disk_usage      = StringField()
    updated         = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        # Serialize Sub Models First

        # Serialize Images Model
        serialized_images = []
        for s_images in self.images:
            serialized_images.append(s_images.serialize())
        
        # Serialize Containers Model
        serialized_containers = []
        for s_containers in self.containers:
            serialized_containers.append(s_containers.serialize())
        
        # Serialize Volumes Model
        serialized_volumes = []
        for s_volumes in self.volumes:
            serialized_volumes.append(s_volumes.serialize())

        # Serialize Networks Model
        serialized_networks = []
        for s_networks in self.networks:
            serialized_networks.append(s_networks.serialize())

        # Return Serilized Objects
        return {
            "id": str(self.id),
            "agent_id": str(self.agent.id),
            "is_installed": self.is_installed,
            "images": serialized_images,
            "containers": serialized_containers,
            "volumes": serialized_volumes,
            "networks": serialized_networks,
            "disk_usage": self.disk_usage,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())

# Docker Info Changelog Model
class ChangeLogDockerInfo(Document):
    docker_info     = ReferenceField(DockerInfo)
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