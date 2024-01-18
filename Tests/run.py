#!/usr/bin/env python3

# Libraries
##############################################################################
from Modules.Register import *
from Modules.Login import *
from Modules.Agent import *
##############################################################################

# Register Tests
##############################################################################
# Invalid Name Test
if test_register_invalid_name():
    print("[SUCCESS]\t[test_register_invalid_name]")
else:
    print("[FAIL]\t[test_register_invalid_name]")

# Invalid Lastname Test
if test_register_invalid_lastname():
    print("[SUCCESS]\t[test_register_invalid_lastname]")
else:
    print("[FAIL]\t[test_register_invalid_lastname]")

# Email Test
if test_register_invalid_email():
    print("[SUCCESS]\t[test_register_invalid_email]")
else:
    print("[FAIL]\t[test_register_invalid_email]")

# Successfuly Register Test
USER_DATA = test_register_success()
if USER_DATA:
    print("[SUCCESS]\t[test_register_success]")
else:
    print("[FAIL]\t[test_register_success]")
##############################################################################

# Login Tests
##############################################################################
# Invalid Email Test
if test_login_invalid_email():
    print("[SUCCESS]\t[test_login_invalid_email]")
else:
    print("[FAIL]\t[test_login_invalid_email]")

# Successfuly Login Test
USER_TOKEN = test_login_success(USER_DATA)
if USER_TOKEN:
    print("[SUCCESS]\t[test_login_success]")
else:
    print("[FAIL]\t[test_login_success]")
##############################################################################

# Agent Tests
##############################################################################
# Wrong Agent Types Test
if test_register_wrong_agent_types(USER_TOKEN):
    print("[SUCCESS]\t[test_register_wrong_agent_types]")
else:
    print("[FAIL]\t[test_register_wrong_agent_types]")

# Double Agent Types Test
if test_register_double_agent_type(USER_TOKEN):
    print("[SUCCESS]\t[test_register_double_agent_type]")
else:
    print("[FAIL]\t[test_register_double_agent_type]")

# Update Wrong Agent Id Test
if test_update_wrong_agent_id(USER_TOKEN):
    print("[SUCCESS]\t[test_update_wrong_agent_id]")
else:
    print("[FAIL]\t[test_update_wrong_agent_id]")

# Successfuly Register Test
AGENT = test_register_agent_success(USER_TOKEN)
if AGENT:
    print("[SUCCESS]\t[test_register_agent_success]")
else:
    print("[FAIL]\t[test_register_agent_success]")

# Successfully Update Agent Type Test
if test_successfully_update_agent_type(AGENT["_id"]["$oid"],USER_TOKEN):
    print("[SUCCESS]\t[test_successfully_update_agent_type]")
else:
    print("[FAIL]\t[test_successfully_update_agent_type]")
##############################################################################