#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import json
from datetime import datetime
from marshmallow import ValidationError

from .models import SystemUsers, ChangeLogSystemUsers
from .schema import RegisterSchema
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_users_bp = Blueprint('sys_users_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Get All System Users
@sys_users_bp.route('/', methods=['GET'])
@auth_token_required
def get_all_system_users():
    try:
        all_sys_users = SystemUsers.objects()

        for sys_users in all_sys_users:
            # Serialize "users" section
            users = []
            for user in sys_users.users:
                users.append(user.serialize())
            # Append again users to System Users
            sys_users.users = users
        
        return [info.serialize() for info in all_sys_users] # Serialize & Return
    except Exception as e:
        return jsonify({"error":str(e)}), 500

# Get System User by Agent ID
@sys_users_bp.route('/<agent_id>', methods=['GET'])
@auth_token_required
def get_system_users_by_agent_id(agent_id):
    try:
        # Get System Users
        sys_users = SystemUsers.objects(agent=agent_id).first()
        
        # Serialize "users" section
        users = []
        for user in sys_users.users:
            users.append(user.serialize())
        
        # Append again users to System Users
        sys_users.users = users
        # Return as serialized
        return jsonify(sys_users.serialize())
    except Exception as e:
        return jsonify({"Message":"Not Found"}), 404

# Register
@sys_users_bp.route('/', methods=['POST'])
@agent_token_required
def register():
    # Get Agent Token by Authorization Header
    agent_token = request.headers.get('Authorization')
    # Get Agent ID by Token
    agent_id = get_id_by_token(agent_token)
    # Get Agent by Agent ID
    agent = Agent.objects(id=agent_id).first()

    # Get Data from Request
    data = request.get_json()

    # Validate the Request
    try:
        # Load and validate the JSON request using the schema
        data = RegisterSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400
        
    # Get if record already exist
    sys_users = SystemUsers.objects(agent=agent).first()

    if sys_users:
        # UPDATE If System Information data already exist
        try:
            # Create SystemUsers object to Compare
            new_users_obj = SystemUsers(**data)
            new_users_obj.agent = agent

            # Find deleted, new, and updated users
            new_users, deleted_users, updated_users = sys_users.compare_users(new_users_obj)
            
            changes = {}

            if deleted_users:
                changes["deleted_users"] = deleted_users
            if new_users:
                changes["new_users"] = new_users
            if updated_users:
                changes["updated_users"] = updated_users

            # If any changes happens
            if changes:
                # Apply updates
                data["updated"] = datetime.utcnow
                sys_users.update(**data)

                # Create a new ChangeLog entry
                change_log_entry = ChangeLogSystemUsers(
                    sys_users = sys_users.id,
                    changes = changes
                )
                change_log_entry.save()
            else:
                # Apply only updated time
                sys_users.update(updated=datetime.utcnow)

        except Exception as e:
            return jsonify({'error': e}), 500
        
    else:
        # CREATE If System Information not exist 
        try:
            sys_users = SystemUsers(**data)
            sys_users.agent = agent
            sys_users.save()
        except Exception as e:
            return jsonify({'error': e}), 500
    
    sys_users_data = json.loads(sys_users.to_json())

    return jsonify(
        {
            'message': 'System users registered successfully.',
            'sys_users': sys_users_data,
        }
    ), 200


# Changelog Routes

# Get All Changelog Data by System Users ID
@sys_users_bp.route('/<sys_users_id>/changelog', methods=['GET'])
@auth_token_required
def get_system_info_changelog_by_sys_users_id(sys_users_id):
    try:
        sys_users_changelog = ChangeLogSystemUsers.objects(sys_users=sys_users_id)
        return [info.serialize() for info in sys_users_changelog] # Serialize & Return
    except Exception as e:
        print(e)
        return jsonify({"Message":"Not Found"}), 404
##############################################################################
