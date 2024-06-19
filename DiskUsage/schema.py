#!/usr/bin/env python3

# Libraries
##############################################################################
from marshmallow import (
    Schema, fields, ValidationError, validates, validates_schema
)

import re
##############################################################################

# Global Values
##############################################################################

##############################################################################

# Regexs
##############################################################################
# Regular expressions optimized to prevent catastrophic backtracking
VALID_DEVICE_REGEX    = r'^(/dev/[a-zA-Z0-9]+|[A-Z]:\\)$'
##############################################################################

# Enums
##############################################################################
class DiskUsageSchema(Schema):
    device      = fields.Str(required=True, validate=lambda s: re.match(VALID_DEVICE_REGEX, s) is not None)
    total_size  = fields.Float(required=True)
    used_size   = fields.Float(required=True)
    free_size   = fields.Float(required=True)

    @validates('total_size')
    def validate_total(self, value):
        if value < 0:
            raise ValidationError('Total disk space must be non-negative')

    @validates('used_size')
    def validate_used(self, value):
        if value < 0:
            raise ValidationError('Used disk space must be non-negative')

    @validates('free_size')
    def validate_free(self, value):
        if value < 0:
            raise ValidationError('Free disk space must be non-negative')

    @validates_schema
    def validate_space(self, data, **kwargs):
        if data['used_size'] + data['free_size'] != data['total_size']:
            raise ValidationError('Sum of used and free space must be equal to total space')
##############################################################################