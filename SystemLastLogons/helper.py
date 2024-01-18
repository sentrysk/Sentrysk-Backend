#!/usr/bin/env python3

# Merge and remove duplicates
##############################################################################
def merge_and_remove_duplicates(list1, list2):
    merged_list = list1 + list2
    unique_records = {}

    for record in merged_list:
        key = (record["username"], record["last_logon"])
        if key not in unique_records:
            unique_records[key] = record

    unique_list = list(unique_records.values())
    return unique_list
##############################################################################