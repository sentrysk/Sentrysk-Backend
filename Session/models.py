#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, StringField, DateTimeField, BooleanField
)
from datetime import datetime, timedelta
##############################################################################

# Configs
##############################################################################

##############################################################################


# Models
##############################################################################
class Session(Document):
    email         = StringField(required=True)
    token         = StringField(required=True, unique=True)
    expire_date   = DateTimeField(default=datetime.utcnow() + timedelta(hours=24))
    is_expired    = BooleanField(required=True, default=False)
    created       = DateTimeField(default=datetime.utcnow)

    def serialize(self):
        return {
            "id":str(self.id),
            "email":self.email,
            "token":self.token,
            "expire_date":self.expire_date,
            "is_expired":self.is_expired,
            "created":self.created
        }
    
    def safe_serialize(self):
        return {
            "email":self.email,
            "created":self.created
        }

    def __str__(self):
        return str(self.serialize())
##############################################################################
