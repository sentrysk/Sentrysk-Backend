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

# Helper Functions
##############################################################################
def compare_documents(old_list, new_list, identifier, cls):
    old_dict = {document[identifier]: document for document in old_list}
    new_dict = {document[identifier]: document for document in new_list}
    
    # Newly Added document
    new_document = [new_dict[identifier] for identifier in new_dict if identifier not in old_dict]
    # Deleted document
    deleted_document = [old_dict[identifier] for identifier in old_dict if identifier not in new_dict]
    # Updated document and Fields
    updated_document = {}

    # Find the Updated Fields
    for identifier in old_dict:
        if identifier in new_dict and old_dict[identifier] != new_dict[identifier]:
            updated_fields = {}
            for field in cls._fields:
                if str(old_dict[identifier][field]) != str(new_dict[identifier][field]):
                    updated_fields[field] = {
                        "previous_value":old_dict[identifier][field],
                        "new_value":new_dict[identifier][field]
                    }
            # Add Updated Fields to Updated document Dict
            updated_document[identifier] = updated_fields

    # Return Compared Data
    return new_document, deleted_document, updated_document
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

    def __eq__(self, other):
        """
        Override the equality operator to compare Images objects.
        """
        return (
            self.image_id == other.image_id and
            self.tags == other.tags and
            self.size == other.size and
            self.created == other.created and
            self.labels == other.labels
        )

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

    def __eq__(self, other):
        """
        Override the equality operator to compare Containers objects.
        """
        return (
            self.container_id == other.container_id and
            self.image == other.image and
            self.status == other.status and
            self.ports == other.ports and
            self.networks == other.networks and
            self.created == other.created and
            self.labels == other.labels
        )

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

    def __eq__(self, other):
        """
        Override the equality operator to compare Volumes objects.
        """
        return (
            self.volume_name == other.volume_name and
            self.mountpoint == other.mountpoint and
            self.created == other.created and
            self.labels == other.labels
        )

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

    def __eq__(self, other):
        """
        Override the equality operator to compare Networks objects.
        """
        return (
            self.network_id == other.network_id and
            self.name == other.name and
            self.driver == other.driver and
            self.created == other.created and
            self.labels == other.labels
        )

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

    def compare_docker_info(self, other):
        if not isinstance(other, DockerInfo):
            raise ValueError("Comparison should be done with another DockerInfo instance")
        
        changes = {}
        # Check Changes on is_installed value
        if self.is_installed != other.is_installed:
            changes['is_installed'] = {}
            changes['is_installed']["previous_value"] = self.is_installed
            changes['is_installed']["new_value"] = other.is_installed
        # Check Changes on disk_usage value
        if self.disk_usage != other.disk_usage:
            changes["disk_usage"] = {}
            changes["disk_usage"]["previous_value"] = self.disk_usage
            changes["disk_usage"]["new_value"] = other.disk_usage
        # Check Changes on Images
        new_images, deleted_images, updated_images = compare_documents(self.images, other.images, "image_id", Images)
        if new_images:
            changes["new_images"] = new_images
        if deleted_images:
            changes["deleted_images"] = deleted_images
        if updated_images:
            changes["updated_images"]  = updated_images
        # Check Changes on Containers
        new_containers, deleted_containers, updated_containers = compare_documents(self.containers, other.containers, "container_id", Containers)
        if new_containers:
            changes["new_containers"] = new_containers
        if deleted_containers:
            changes["deleted_containers"] = deleted_containers
        if updated_containers:
            changes["updated_containers"]  = updated_containers
        # Check Changes on Volumes
        new_volumes, deleted_volumes, updated_volumes = compare_documents(self.volumes, other.volumes, "volume_name", Volumes)
        if new_volumes:
            changes["new_volumes"] = new_volumes
        if deleted_volumes:
            changes["deleted_volumes"] = deleted_volumes
        if updated_volumes:
            changes["updated_volumes"]  = updated_volumes
        # Check Changes on Networks
        new_networks, deleted_networks, updated_networks = compare_documents(self.networks, other.networks, "network_id", Networks)
        if new_networks:
            changes["new_networks"] = new_networks
        if deleted_networks:
            changes["deleted_networks"] = deleted_networks
        if updated_networks:
            changes["updated_networks"]  = updated_networks
        
        return changes

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