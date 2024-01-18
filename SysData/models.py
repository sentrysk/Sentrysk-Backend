#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, StringField, IntField, FloatField, BooleanField,
    ListField, EmbeddedDocument, EmbeddedDocumentField
)
from datetime import datetime, timedelta
##############################################################################


# Models
##############################################################################
# Define the data models
class Os(EmbeddedDocument):
    system = StringField()
    release = StringField()
    version = StringField()

class Domain(EmbeddedDocument):
    domain = StringField()
    dns_hostname = StringField()

class Cpu(EmbeddedDocument):
    cpu = StringField()
    cpu_cores = IntField()
    cpu_threads = IntField()

class Memory(EmbeddedDocument):
    total_memory = StringField()
    available_memory = StringField()
    memory_percent = FloatField()

class Disk(EmbeddedDocument):
    device = StringField()
    mountpoint = StringField()
    filesystem = StringField()
    total_size = StringField()
    used_size = StringField()
    free_size = StringField()
    usage_percent = FloatField()
    bitlocker_status = StringField()

class NetworkAddress(EmbeddedDocument):
    type = StringField()
    ip_address = StringField()
    netmask = StringField()
    broadcast = StringField()

class NetworkInterface(EmbeddedDocument):
    name = StringField()
    addresses = ListField(EmbeddedDocumentField(NetworkAddress))
    mac_address = StringField()

class UserData(EmbeddedDocument):
    name = StringField()
    sid = StringField()

class AuditPolicy(EmbeddedDocument):
    category = StringField()
    subcategory = StringField()
    setting = StringField()
    success = BooleanField()

class InstalledProgram(EmbeddedDocument):
    name = StringField()
    version = StringField()

class Service(EmbeddedDocument):
    node = StringField()
    displayname = StringField()
    name = StringField()
    pathname = StringField()
    startmode = StringField()
    state = StringField()

class UpdateHistory(EmbeddedDocument):
    title = StringField()
    description = StringField()
    operation = IntField()
    result_code = IntField()
    date = StringField()

class MissingUpdate(EmbeddedDocument):
    title = StringField()
    description = StringField()
    category = StringField()

class Image(EmbeddedDocument):
    image_id = StringField()
    tags = ListField(StringField())
    size = StringField()
    created = StringField()
    labels = StringField()

class Container(EmbeddedDocument):
    container_id = StringField()
    image = StringField()
    status = StringField()
    ports = StringField()
    networks = StringField()
    created = StringField()
    labels = StringField()

class Volume(EmbeddedDocument):
    volume_name = StringField()
    mountpoint = StringField()
    created = StringField()
    labels = StringField()

class Network(EmbeddedDocument):
    network_id = StringField()
    name = StringField()
    driver = StringField()
    created = StringField()
    labels = StringField()

class DiskUsage(EmbeddedDocument):
    total_space = StringField()

class NpmPackage(EmbeddedDocument):
    name = StringField()
    version = StringField()

class PipPackage(EmbeddedDocument):
    name = StringField()
    version = StringField()

class DockerInfo(EmbeddedDocument):
    running = BooleanField()
    images = ListField(EmbeddedDocumentField(Image))
    containers = ListField(EmbeddedDocumentField(Container))
    volumes = ListField(EmbeddedDocumentField(Volume))
    networks = ListField(EmbeddedDocumentField(Network))
    disk_usage = EmbeddedDocumentField(DiskUsage)

class NpmInfo(EmbeddedDocument):
    running = BooleanField()
    packages = ListField(EmbeddedDocumentField(NpmPackage))

class PipInfo(EmbeddedDocument):
    installed = BooleanField()
    packages = ListField(EmbeddedDocumentField(PipPackage))

class System(EmbeddedDocument):
    os = EmbeddedDocumentField(Os)
    domain = EmbeddedDocumentField(Domain)
    cpu = EmbeddedDocumentField(Cpu)
    memory = EmbeddedDocumentField(Memory)
    disks = ListField(EmbeddedDocumentField(Disk))
    network_interfaces = ListField(EmbeddedDocumentField(NetworkInterface))

class Data(Document):
    system =  EmbeddedDocumentField(System)
    users = ListField(EmbeddedDocumentField(UserData))
    audit_policies = ListField(EmbeddedDocumentField(AuditPolicy))
    installed_programs = ListField(EmbeddedDocumentField(InstalledProgram))
    services = ListField(EmbeddedDocumentField(Service))
    update_history = ListField(EmbeddedDocumentField(UpdateHistory))
    missing_updates = ListField(EmbeddedDocumentField(MissingUpdate))
    docker_info = EmbeddedDocumentField(DockerInfo)
    npm_info = EmbeddedDocumentField(NpmInfo)
    pip_info = EmbeddedDocumentField(PipInfo)
##############################################################################
