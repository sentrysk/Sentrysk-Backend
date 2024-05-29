#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from .models import AgentConfig
from .schema import AgentConfigRegisterSchema
from Shared.validators import auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
agnt_configs_bp = Blueprint('agent_configs_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Register
@agnt_configs_bp.route('/', methods=['POST'])
@auth_token_required
def register():
    # Get Agent Token by Authorization Header
    agent_token = request.headers.get('Authorization')
    # Get Agent ID by Token
    agent_id = get_id_by_token(agent_token)
    # Get Agent by Agent ID
    agent = Agent.objects(id=agent_id).first()

    try:
        # Load and validate the JSON request using the schema
        data = AgentConfigRegisterSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400

    # Get Agent ID by Token
    agent_config = AgentConfig().objects(agent=agent).first()

    if agent_config:
        # UPDATE If Agent Config already exist
        data["updated"] = datetime.utcnow
        agent_config.update(**data)
    else:
        # CREATE If Agent Config not exist
        try:
            agent_config = AgentConfig(**data)
            agent_config.agent = agent
            agent_config.save()
        except Exception as e:
            return jsonify({'error': e}), 500


    return jsonify(
        {
            'message': 'Agent Config registered successfully.',
        }
    ), 200
##############################################################################
