#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from Shared.validators import agent_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
disk_usage_bp = Blueprint('disk_usage_blueprint', __name__)
##############################################################################

# Routes
##############################################################################


# Register
@disk_usage_bp.route('/', methods=['POST'])
@agent_token_required
def register():
    pass

##############################################################################
