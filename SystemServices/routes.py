#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from .models import SystemServices, ChangeLogSystemServices
from .schema import RegisterSchema
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_srvc_bp = Blueprint('sys_services_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Get All System Services
@sys_srvc_bp.route('/', methods=['GET'])
@auth_token_required
def get_all_system_services():
    try:
        # Get All System Services from DB
        all_sys_srvcs = SystemServices.objects()
        # Serialize & Return
        return [info.serialize() for info in all_sys_srvcs]
    except Exception as e:
        return jsonify({"error":str(e)}), 500

# Get System Services by Agent ID
@sys_srvc_bp.route('/<agent_id>', methods=['GET'])
@auth_token_required
def get_system_services_by_agent_id(agent_id):
    try:
        # Get System Services by Agent ID
        sys_srvcs = SystemServices.objects(agent=agent_id).first().serialize()
        # Return the System Services
        return jsonify(sys_srvcs)
    except Exception as e:
        return jsonify({"Message":"Not Found"}), 404

# Register
@sys_srvc_bp.route('/', methods=['POST'])
@agent_token_required
def register():
    # Get Agent Token by Authorization Header
    agent_token = request.headers.get('Authorization')
    # Get Agent ID by Token
    agent_id = get_id_by_token(agent_token)
    # Get Agent by Agent ID
    agent = Agent.objects(id=agent_id).first()

    try:
        # Load and validate the JSON request using the schema
        data = RegisterSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400
        
    # Get Services if record already exist
    sys_srvcs = SystemServices.objects(agent=agent).first()

    if sys_srvcs:
        # UPDATE If System Information data already exist
        try:
            # Create SystemServices object to Compare
            new_srvcs_obj = SystemServices(**data)
            new_srvcs_obj.agent = agent

            # Find deleted, new, and updated services
            new_services, deleted_services, updated_services = sys_srvcs.compare_servies(new_srvcs_obj)
            
            changes = {}

            if deleted_services:
                changes["deleted_services"] = deleted_services
            if new_services:
                changes["new_services"] = new_services
            if updated_services:
                changes["updated_services"] = updated_services

            # If any changes happens
            if changes:
                # Apply updates
                data["updated"] = datetime.utcnow
                sys_srvcs.update(**data)

                # Create a new ChangeLog entry
                change_log_entry = ChangeLogSystemServices(
                    services = sys_srvcs.id,
                    changes = changes
                )
                change_log_entry.save()
            else:
                # Apply only updated time
                sys_srvcs.update(updated=datetime.utcnow)

        except Exception as e:
            return jsonify({'error': e}), 500
        
    else:
        # CREATE If System Services not exist 
        try:
            sys_srvcs = SystemServices(**data)
            sys_srvcs.agent = agent
            sys_srvcs.save()
        except Exception as e:
            return jsonify({'error': e}), 500

    return jsonify(
        {
            'message': 'System Services registered successfully.',
        }
    ), 200

# Changelog Routes

# Get All Changelog Data by System Services ID
@sys_srvc_bp.route('/<sys_srvcs_id>/changelog', methods=['GET'])
@auth_token_required
def get_sys_srvcs_changelog_by_sys_srvcs_id(sys_srvcs_id):
    try:
        sys_srvcs_changelog = ChangeLogSystemServices.objects(services=sys_srvcs_id)
        return [info.serialize() for info in sys_srvcs_changelog] # Serialize & Return
    except Exception as e:
        print(e)
        return jsonify({"Message":"Not Found"}), 404
##############################################################################
