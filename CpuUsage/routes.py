#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError
from bson import ObjectId

from .schema import RegisterSchema
from .models import CpuUsage
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
cpu_usage_bp = Blueprint('cpu_usage_blueprint', __name__)
##############################################################################

# Routes
##############################################################################

# Register
@cpu_usage_bp.route('/', methods=['POST'])
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

    # Register CPU Usage Data
    try:
        memory_usage = CpuUsage(**data)
        memory_usage.agent = agent
        memory_usage.save()
    except Exception as e:
        return jsonify({'error': e}), 500

    return jsonify(
        {
            'message': 'CPU Usage registered successfully.',
        }
    ), 200
##############################################################################
