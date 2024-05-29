#!/usr/bin/env python3

# Libraries
##############################################################################

# Functions
##############################################################################

# Find Changes between to Agent Config
def get_changes(old, new):
    changes = {}
    ignore_fields = {'_id', 'updated'}

    for key in new:
        if key in ignore_fields:
            continue
        old_value = old.get(key)
        new_value = new[key]
        if isinstance(new_value, dict) and isinstance(old_value, dict):
            sub_changes = get_changes(old_value, new_value)
            if sub_changes:
                changes[key] = sub_changes
        else:
            if old_value != new_value:
                changes[key] = {'previous_value': old_value, 'new_value': new_value}

    for key in old:
        if key in ignore_fields:
            continue
        if key not in new:
            changes[key] = {'previous_value': old[key], 'new_value': None}

    return changes

##############################################################################