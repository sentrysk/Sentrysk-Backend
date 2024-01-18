#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, jsonify, request

from Shared.validators import auth_token_required
from .models import Session
##############################################################################

# Blueprint
##############################################################################
session_bp = Blueprint('session_blueprint', __name__)
##############################################################################


# Routes
##############################################################################

# Session Check
@session_bp.route('/check', methods=['GET'])
@auth_token_required
def check_session():
    return jsonify({"message":"Session active"}),200

# Get Previous Session
@session_bp.route('/prev_sessions', methods=['GET'])
@auth_token_required
def get_personal_prev_sessions():
    # Get Token from Auth Header
    auth_header = request.headers.get('Authorization')
    # Get User ID from token
    user_email = Session.objects(token=auth_header).first()['email']
    # Get Sessions belongs to this
    sessions = Session.objects(email=user_email, is_expired=True)
    # Create Empty Previous Sessions List
    prev_sessions = []
    # Serialize the Sessions
    for session in sessions:
        prev_sessions.append(session.safe_serialize())
    
    # Return the List of Previous Sessions
    return jsonify(prev_sessions),200
##############################################################################
