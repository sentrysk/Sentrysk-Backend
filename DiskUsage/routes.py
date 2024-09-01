#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError
from bson import ObjectId

from .schema import RegisterSchema
from .models import DiskUsage
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
disk_usage_bp = Blueprint('disk_usage_blueprint', __name__)
##############################################################################

# Routes
##############################################################################

# Disk Usage by Agent ID
@disk_usage_bp.route('/<agent_id>/latest', methods=['GET'])
@auth_token_required
def get_latest_disk_usage_by_agent_id(agent_id):
    try:
        # Fetch devices from the DiskUsage collection filtered by agent ID
        devices = DiskUsage.objects(agent=ObjectId(agent_id)).distinct('device')

        if devices:
            # Create Usage List
            disk_usage_list = []
            # Iterate over devices
            for device in devices:
                # Get latest usage for every device
                latest_usage = DiskUsage.objects(
                    agent  = ObjectId(agent_id),
                    device = device
                ).order_by('-timestamp').first()
                # Append usage data to list
                disk_usage_list.append(latest_usage.serialize())
            
            return jsonify(disk_usage_list),200
        return jsonify({'Error':'Latest disk usage not found'}),404
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Disk Usage by Agent ID
@disk_usage_bp.route('/<agent_id>', methods=['GET'])
@auth_token_required
def get_disk_usage_by_agent_id(agent_id):
    try:
        # Fetch records from the DiskUsage collection filtered by agent ID
        records = DiskUsage.objects(agent=ObjectId(agent_id))
        # Convert the records to JSON
        response_data = [record.serialize() for record in records]
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Register
@disk_usage_bp.route('/', methods=['POST'])
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
        # Iterate over disk usage data list
        for disk_usage_data in data["disk_usage"]:
            disk_usage = DiskUsage(**disk_usage_data)
            disk_usage.agent = agent
            disk_usage.percent = (disk_usage.used_size / disk_usage.total_size) * 100
            disk_usage.free_size = disk_usage.total_size - disk_usage.used_size
            disk_usage.save()
    except Exception as e:
        return jsonify({'error': e}), 500

    return jsonify(
        {
            'message': 'Disk Usage registered successfully.',
        }
    ), 200
##############################################################################
