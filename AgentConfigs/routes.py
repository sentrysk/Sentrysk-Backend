#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import json
from marshmallow import ValidationError

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



##############################################################################
