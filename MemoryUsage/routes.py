#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError
from bson import ObjectId

from .schema import RegisterSchema
from .models import MemoryUsage
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
memory_usage_bp = Blueprint('memory_usage_blueprint', __name__)
##############################################################################

# Routes
##############################################################################

# Get Memory Usage by Agent ID
@memory_usage_bp.route('/<agent_id>', methods=['GET'])
@auth_token_required
def get_memory_usage_by_agent_id(agent_id):
    try:
        # Fetch records from the MemoryUsage collection filtered by agent ID
        records = MemoryUsage.objects(agent=ObjectId(agent_id))
        # Convert the records to JSON
        response_data = [record.serialize() for record in records]
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Register
@memory_usage_bp.route('/', methods=['POST'])
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

    # Register Disk Usage Data
    try:
        memory_usage = MemoryUsage(**data)
        memory_usage.agent = agent
        memory_usage.percent = (memory_usage.used_size / memory_usage.total_size) * 100
        memory_usage.free_size = memory_usage.total_size - memory_usage.used_size
        memory_usage.save()
    except Exception as e:
        return jsonify({'error': e}), 500

    return jsonify(
        {
            'message': 'Memory Usage registered successfully.',
        }
    ), 200
##############################################################################
