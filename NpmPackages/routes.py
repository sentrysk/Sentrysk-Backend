#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from .models import InstalledNpmPackages, ChangeLogInstalledNpmPackages
from .schema import RegisterSchema
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
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

# Register
@sys_npm_pkgs_bp.route('/', methods=['POST'])
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
        
    # Get if record already exist
    npm_pkgs = InstalledNpmPackages.objects(agent=agent).first()

    if npm_pkgs:
        # UPDATE If System Information data already exist
        try:
            # Create InstalledNpmPackages object to Compare
            new_npm_pkgs_obj = InstalledNpmPackages(**data)
            new_npm_pkgs_obj.agent = agent

            # Find deleted, new, and updated npm_pkgs
            new_npm_pkgs, deleted_npm_pkgs, updated_npm_pkgs = npm_pkgs.compare_npm_pkgs(new_npm_pkgs_obj)
            
            changes = {}

            if deleted_npm_pkgs:
                changes["deleted_npm_pkgs"] = deleted_npm_pkgs
            if new_npm_pkgs:
                changes["new_npm_pkgs"] = new_npm_pkgs
            if updated_npm_pkgs:
                changes["updated_npm_pkgs"] = updated_npm_pkgs

            # If any changes happens
            if changes:
                # Apply updates
                data["updated"] = datetime.utcnow
                npm_pkgs.update(**data)

                # Create a new ChangeLog entry
                change_log_entry = ChangeLogInstalledNpmPackages(
                    pip_packages = npm_pkgs.id,
                    changes = changes
                )
                change_log_entry.save()
            else:
                # Apply only updated time
                npm_pkgs.update(updated=datetime.utcnow)

        except Exception as e:
            return jsonify({'error': e}), 500
        
    else:
        # CREATE If System Installed npm_packages not exist 
        try:
            npm_pkgs = InstalledNpmPackages(**data)
            npm_pkgs.agent = agent
            npm_pkgs.save()
        except Exception as e:
            return jsonify({'error': e}), 500

    return jsonify(
        {
            'message': 'Npm packages registered successfully.',
        }
    ), 200

# Get All Changelog Data by Npm Packages ID
@sys_npm_pkgs_bp.route('/<npm_pkgs_id>/changelog', methods=['GET'])
@auth_token_required
def get_npm_pkgs_changelog_by_npm_pkgs_id(npm_pkgs_id):
    try:
        npm_pkgs_changelog = ChangeLogInstalledNpmPackages.objects(npm_packages=npm_pkgs_id)
        return [info.serialize() for info in npm_pkgs_changelog] # Serialize & Return
    except Exception as e:
        print(e)
        return jsonify({"Message":"Not Found"}), 404
##############################################################################