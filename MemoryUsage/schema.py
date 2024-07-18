#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import (
    Schema, fields, ValidationError, validates, validates_schema
)

##############################################################################

# Schemas
##############################################################################
class MemoryUsageSchema(Schema):
    total_size  = fields.Float(required=True)
    used_size   = fields.Float(required=True)

    @validates('total_size')
    def validate_total(self, value):
        if value < 0:
            raise ValidationError('Total memory space must be non-negative')

    @validates('used_size')
    def validate_used(self, value):
        if value < 0:
            raise ValidationError('Used memory space must be non-negative')
        
    @validates_schema
    def validate_space(self, data, **kwargs):
        if data['used_size'] > data['total_size']:
            raise ValidationError('Used memory space can not bigger than total space')
##############################################################################