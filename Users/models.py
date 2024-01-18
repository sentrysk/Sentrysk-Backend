#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, StringField, DateTimeField, BinaryField
)
from datetime import datetime
##############################################################################

# Models
##############################################################################
class User(Document):
    name      = StringField(required=True)
    lastname  = StringField(required=True)
    email     = StringField(required=True, unique=True)
    password  = BinaryField(required=True)
    created   = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        return {
            "id":str(self.id),
            "name":self.name,
            "lastname":self.lastname,
            "email":self.email,
            "password":self.password,
            "created":self.created
        }
    
    def safe_serialize(self):
        return {
            "id":str(self.id),
            "name":self.name,
            "lastname":self.lastname,
            "email":self.email,
            "created":self.created
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################
