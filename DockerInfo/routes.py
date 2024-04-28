#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from .models import DockerInfo
from .schema import RegisterSchema
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_dckr_bp = Blueprint('sys_docker_blueprint', __name__)
##############################################################################

# Routes
##############################################################################

# Get All Docker Infor from All Agents
@sys_dckr_bp.route('/<agent_id>', methods=['GET'])
@auth_token_required
def get_docker_info_by_agent_id():
    try:
        # Get All Docker Info from DB
        all_docker_infos = DockerInfo.objects()
        # Serialize & Return
        return [info.serialize() for info in all_docker_infos] 
    except Exception as e:
        return jsonify({"error":str(e)}), 500

# Get Docker Info by Agent ID
@sys_dckr_bp.route('/<agent_id>', methods=['GET'])
@auth_token_required
def get_docker_info_by_agent_id(agent_id):
    try:
        # Get Docker Info by Agent ID & Serialize
        docker_info = DockerInfo.objects(agent=agent_id).first().serialize()
        # Return the Npm Packages
        return jsonify(docker_info)
    except Exception as e:
        return jsonify({"Message":str(e)}), 404

# Register
@sys_dckr_bp.route('/', methods=['POST'])
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
        
    # Get if record already exist
    docker_info = DockerInfo.objects(agent=agent).first()

    if docker_info:
        # UPDATE If System Information data already exist
        try:
            docker_info.update(updated=datetime.utcnow)
        except Exception as e:
            return jsonify({'error': e}), 500
        
    else:
        # CREATE If Docker Info not exist 
        try:
            docker_info = DockerInfo(**data)
            docker_info.agent = agent
            docker_info.save()
        except Exception as e:
            return jsonify({'error': e}), 500

    return jsonify(
        {
            'message': 'Docker Info registered successfully.',
        }
    ), 200
##############################################################################