#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, jsonify

from .models import InstalledNpmPackages
from Shared.validators import auth_token_required
##############################################################################

# Blueprint
##############################################################################
sys_npm_pkgs_bp = Blueprint('sys_npm_pkgs_blueprint', __name__)
##############################################################################

# Routes
##############################################################################

# Get All Npm Packages from All Agents
@sys_npm_pkgs_bp.route('/', methods=['GET'])
@auth_token_required
def get_all_installed_npm_packages():
    try:
        # Get All Npm Packages from DB
        all_npm_pkgs = InstalledNpmPackages.objects()
        # Serialize & Return
        return [info.serialize() for info in all_npm_pkgs] 
    except Exception as e:
        return jsonify({"error":str(e)}), 500

# Get Npm Packages by Agent ID
@sys_npm_pkgs_bp.route('/<agent_id>', methods=['GET'])
@auth_token_required
def get_npm_packages_by_agent_id(agent_id):
    try:
        # Get All Npm Packages by Agent ID & Serialize
        npm_pkgs = InstalledNpmPackages.objects(agent=agent_id).first().serialize()
        # Return the Npm Packages
        return jsonify(npm_pkgs)
    except Exception as e:
        return jsonify({"Message":str(e)}), 404

##############################################################################