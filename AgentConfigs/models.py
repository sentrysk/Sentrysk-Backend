#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, DictField, ReferenceField, DateTimeField, ListField,
    EmbeddedDocument, EmbeddedDocumentField, StringField, IntField
)
from datetime import datetime
##############################################################################


# Models
##############################################################################
class Endpoints(EmbeddedDocument):
    system_info        = StringField(required=True)
    user_info          = StringField(required=True)
    installed_programs = StringField(required=True)
    service_info       = StringField(required=True)
    last_logons        = StringField(required=True)
    pip_pkgs           = StringField(required=True)
    npm_pkgs           = StringField(required=True)
    docker_info        = StringField(required=True)


##############################################################################
