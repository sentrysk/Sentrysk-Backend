#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify

from .models import DockerInfo
from Shared.validators import agent_token_required, auth_token_required

from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_dckr_bp = Blueprint('sys_docker_blueprint', __name__)
##############################################################################

# Routes
##############################################################################

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

##############################################################################