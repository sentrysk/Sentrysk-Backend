#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from .models import AgentConfig, ChangeLogAgentConfig
from .schema import AgentConfigRegisterSchema
from .helper_funcs import get_changes
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
agnt_configs_bp = Blueprint('agent_configs_blueprint', __name__)
##############################################################################

# Routes
##############################################################################

# Get All Agent Configs
@agnt_configs_bp.route('/', methods=['GET'])
@auth_token_required
def get_agent_configs():
    try:
        agent_configs = AgentConfig.objects()
        return [agent_config.serialize() for agent_config in agent_configs] # Serialize & Return
    except Exception as e:
        return jsonify({"error":str(e)}), 500

# Get Agent Config by ID
@agnt_configs_bp.route('/<id>', methods=['GET'])
def get_agent_config_by_id(id):
    try:
        agent_config = AgentConfig.objects(id=id).first().serialize()
        return jsonify(agent_config)
    except Exception as e:
        return jsonify({"Message":"Not Found"}), 404
    
# Get Agent Config by Agent ID
@agnt_configs_bp.route('/<agent_id>', methods=['GET'])
def get_agent_config_by_id(agent_id):
    try:
        agent_config = AgentConfig.objects(agent=agent_id).first().serialize()
        return jsonify(agent_config)
    except Exception as e:
        return jsonify({"Message":"Not Found"}), 404

# Register
@agnt_configs_bp.route('/', methods=['POST'])
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
        data = AgentConfigRegisterSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400

    # Get Agent ID by Token
    agent_config = AgentConfig.objects(agent=agent).first()

    if agent_config:
        # UPDATE If Agent Config already exist

        # Convert to dict to compare
        old_config = agent_config.to_mongo().to_dict()

        # Create Temp object to compare
        tmp_agnt_cfg = AgentConfig(**data)
        tmp_agnt_cfg.agent = agent
        tmp_agnt_cfg = tmp_agnt_cfg.to_mongo().to_dict() # Convert to dict
        
        changes = get_changes(old_config, tmp_agnt_cfg)

        # If any changes
        if changes:
            # Update the existing SystemInfo document
            data["updated"] = datetime.utcnow
            agent_config.update(**data)

            # Create a new ChangeLog entry
            change_log_entry = ChangeLogAgentConfig(
                agent_config = agent_config.id,
                changes = changes
            )
            change_log_entry.save()
        else:
            # Apply only updated time
            agent_config.update(updated=datetime.utcnow)
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
