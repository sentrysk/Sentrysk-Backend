#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import json
from marshmallow import ValidationError
from datetime import datetime

from .models import SystemInfo, ChangeLogSystemInfo
from .schema import RegisterSchema,UpdateSchema
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_info_bp = Blueprint('sys_info_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Get All System Data
@sys_info_bp.route('/', methods=['GET'])
@auth_token_required
def get_all_system_info():
    try:
        sys_info = SystemInfo.objects()
        return [info.serialize() for info in sys_info] # Serialize & Return
    except Exception as e:
        return jsonify({"error":str(e)}), 500
    
# Get All System Data
@sys_info_bp.route('/<agent_id>', methods=['GET'])
@auth_token_required
def get_system_info_by_agent_id(agent_id):
    try:
        sys_info = SystemInfo.objects(agent=agent_id).first().serialize()
        return jsonify(sys_info)
    except Exception as e:
        return jsonify({"Message":"Not Found"}), 404

# Register
@sys_info_bp.route('/', methods=['POST'])
@agent_token_required
def register():
    # Get Agent Token by Authorization Header
    agent_token = request.headers.get('Authorization')
    # Get Agent ID by Token
    agent_id = get_id_by_token(agent_token)
    # Get Agent by Agent ID
    agent = Agent.objects(id=agent_id).first()

    # Get if record already exist
    sys_info = SystemInfo.objects(agent=agent).first()

    if sys_info:
        # UPDATE If System Information data already exist 
        
        # Get Data and Validate Request
        try:
            # Load and validate the JSON request using the schema
            data = UpdateSchema().load(request.json)
        except ValidationError as e:
            # Return validation errors as a JSON response with a 400 status code
            return jsonify({'error': e.messages}), 400
        
        changes = {}

        for field, new_value in data.items():
            if field in sys_info._data and sys_info[field] != new_value:
                changes[field] = {
                    'previous_value': sys_info[field],
                    'new_value': new_value
                }

        # If any changes
        if changes:
            # Update the existing SystemInfo document
            data["updated"] = datetime.utcnow
            sys_info.update(**data)
            
            # Create a new ChangeLog entry
            change_log_entry = ChangeLogSystemInfo(
                system_info = sys_info.id,
                changes = changes
            )
            change_log_entry.save()
        else:
            # Apply only updated time
            sys_info.update(updated=datetime.utcnow)
    else:
        # CREATE If System Information not exist 
        
        # Get Data and Validate Request
        try:
            # Load and validate the JSON request using the schema
            data = RegisterSchema().load(request.json)
        except ValidationError as e:
            # Return validation errors as a JSON response with a 400 status code
            return jsonify({'error': e.messages}), 400

        os                  = data.get('os')
        domain              = data.get('domain')
        cpu                 = data.get('cpu')
        memory              = data.get('memory')
        disks               = data.get('disks')
        network_interfaces  = data.get('network_interfaces')

        # Register System Info to DB
        sys_info = SystemInfo(
            agent = agent,
            os = os, 
            domain=domain,
            cpu = cpu,
            memory = memory,
            disks = disks,
            network_interfaces = network_interfaces
        )
        sys_info.save()
    
    sys_info_data = json.loads(sys_info.to_json())

    return jsonify(
        {
            'message': 'System info registered successfully.',
            'sys_info': sys_info_data,
        }
    ), 200


# Changelog Routes

# Get All Changelog Data by System Info ID
@sys_info_bp.route('/<sys_info_id>/changelog', methods=['GET'])
@auth_token_required
def get_system_info_changelog_by_sys_info_id(sys_info_id):
    try:
        sys_info_changelog = ChangeLogSystemInfo.objects(system_info=sys_info_id)
        return [info.serialize() for info in sys_info_changelog] # Serialize & Return
    except Exception as e:
        print(e)
        return jsonify({"Message":"Not Found"}), 404
##############################################################################
