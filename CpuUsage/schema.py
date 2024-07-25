#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import (
    Schema, fields, ValidationError, validates
)

##############################################################################

# Schemas
##############################################################################
class RegisterSchema(Schema):
    cpu_usage  = fields.Float(required=True)

    @validates('cpu_usage')
    def validate_total(self, value):
        if value < 0:
            raise ValidationError('Cpu Usage must be non-negative')

##############################################################################