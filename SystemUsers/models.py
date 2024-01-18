#!/usr/bin/env python3

# Libraries
##############################################################################
from mongoengine import (
    Document, DictField, ReferenceField,  DateTimeField,  ListField,
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
class UserData(EmbeddedDocument):
    username        = StringField()
    user_id         = StringField()
    group_id        = StringField()
    home_directory  = StringField()
    shell           = StringField()
    full_name       = StringField()
    comment         = StringField()
    flags           = ListField()
    sid             = StringField()

    def __eq__(self, other):
        return (
            self.username == other.username and
            self.user_id == other.user_id and
            self.group_id == other.group_id and
            self.home_directory == other.home_directory and
            self.shell == other.shell and
            self.full_name == other.full_name and
            self.comment == other.comment and
            self.flags == other.flags and
            self.sid == other.sid
        )

    @staticmethod
    def normalize_datetime(dt):
        if dt:
            
            if isinstance(dt, datetime):
                # If dt is already a datetime instance
                return dt.strftime(DATE_FORMAT)
            else:
                # If dt is not a datetime instance, its Str or something...
                return datetime.strftime(datetime.strptime(dt,DATE_FORMAT),DATE_FORMAT)
        else:
            return dt

    def serialize(self):
        data = {
            "username": self.username
        }
        if self.user_id:
            data["user_id"] = self.user_id
        if self.group_id:
            data["group_id"] = self.group_id
        if self.home_directory:
            data["home_directory"] = self.home_directory
        if self.shell:
            data["shell"] = self.shell
        if self.full_name:
            data["full_name"] = self.full_name
        if self.comment:
            data["comment"] = self.comment
        if self.flags:
            data["flags"] = self.flags
        if self.sid:
            data["sid"] = self.sid

        return data

    def __str__(self):
        return str(self.serialize())

class SystemUsers(Document):
    agent               = ReferenceField(Agent)
    users               = ListField(EmbeddedDocumentField(UserData))
    updated             = DateTimeField(default=datetime.utcnow)

    # To compare 2 Users Data
    def compare_users(self, other):
        if not isinstance(other, SystemUsers):
            raise ValueError("Comparison should be done with another SystemUsers instance")

        self_users = {user.username: user for user in self.users}
        other_users = {user.username: user for user in other.users}

        # Newly Added Users
        new_users = [user.serialize() for username, user in other_users.items() if username not in self_users]
        # Deleted Users
        deleted_users = [user.serialize() for username, user in self_users.items() if username not in other_users]
        # Updated Users and Fields
        updated_users = {}

        # Find the Updated Fields
        for username in self_users:
            if username in other_users and self_users[username] != other_users[username]:
                updated_fields = {}
                for field in UserData._fields:
                    if str(self_users[username][field]) != str(other_users[username][field]):
                        updated_fields[field] = {
                            "previous_value":self_users[username][field],
                            "new_value":other_users[username][field]
                        }
                # Add Updated Fields to Updated Users Dict
                updated_users[username] = updated_fields

        # Return Compared Data
        return new_users, deleted_users, updated_users
    
    def serialize(self):
        return {
            "id":str(self.id),
            "agent_id":str(self.agent.id),
            "users":self.users,
            "updated":self.updated
        }

    def __str__(self):
        return str(self.serialize())

class ChangeLogSystemUsers(Document):
    sys_users       = ReferenceField(SystemUsers)
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