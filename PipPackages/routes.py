#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from .models import InstalledPipPackages, ChangeLogInstalledPipPackages
from .schema import RegisterSchema
from Shared.validators import agent_token_required, auth_token_required

from Agents.helper_funcs import get_id_by_token
from Agents.models import Agent
##############################################################################

# Blueprint
##############################################################################
sys_pip_pkgs_bp = Blueprint('sys_pip_pkgs_blueprint', __name__)
##############################################################################

# Routes
##############################################################################

# Get All Pip Packages from All Agents
@sys_pip_pkgs_bp.route('/', methods=['GET'])
@auth_token_required
def get_all_installed_pip_packages():
    try:
        # Get All Pip Packages from DB
        all_pip_pkgs = InstalledPipPackages.objects()
        # Serialize & Return
        return [info.serialize() for info in all_pip_pkgs] 
    except Exception as e:
        return jsonify({"error":str(e)}), 500
    
# Get All Pip Packages Formatted
@sys_pip_pkgs_bp.route('/formatted', methods=['GET'])
@auth_token_required
def get_all_pip_packages_formatted():
    try:
        # Get All System Apps from DB
        all_pip_pkgs = InstalledPipPackages.objects()
        # Create Apps Dict to Store Formatted Data
        pip_pkgs_dict = {}
        # Iterate over agents 
        for pip_pkgs in all_pip_pkgs:
            # Iterate over apps
            for pip_pkg in pip_pkgs.pip_packages:
                # Check whether app already exist
                if pip_pkgs_dict.get(pip_pkg.name):
                    # Check whether app version already exist
                    if pip_pkgs_dict[pip_pkg.name].get(pip_pkg.version):
                        pip_pkgs_dict[pip_pkg.name][pip_pkg.version].append(pip_pkgs.agent.serialize()["id"])
                    else:
                        pip_pkgs_dict[pip_pkg.name][pip_pkg.version] = [pip_pkgs.agent.serialize()["id"]]
                else:
                    # If not exist create new one
                    pip_pkgs_dict[pip_pkg.name] = {}
                    pip_pkgs_dict[pip_pkg.name][pip_pkg.version] = [pip_pkgs.agent.serialize()["id"]]

        # Serialize & Return
        return jsonify(pip_pkgs_dict)
    except Exception as e:
        return jsonify({"error":str(e)}), 500

# Get All Pip Packages by Agent ID
@sys_pip_pkgs_bp.route('/<agent_id>', methods=['GET'])
@auth_token_required
def get_pip_packages_by_agent_id(agent_id):
    try:
        # Get All Pip Packages by Agent ID & Serialize
        pip_pkgs = InstalledPipPackages.objects(agent=agent_id).first().serialize()
        # Return the Pip Packages
        return jsonify(pip_pkgs)
    except Exception as e:
        return jsonify({"Message":str(e)}), 404

# Register
@sys_pip_pkgs_bp.route('/', methods=['POST'])
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
    pip_pkgs = InstalledPipPackages.objects(agent=agent).first()

    if pip_pkgs:
        # UPDATE If System Information data already exist
        try:
            # Create InstalledPipPackages object to Compare
            new_pip_pkgs_obj = InstalledPipPackages(**data)
            new_pip_pkgs_obj.agent = agent

            # Find deleted, new, and updated pip_pkgs
            new_pip_pkgs, deleted_pip_pkgs, updated_pip_pkgs = pip_pkgs.compare_pip_pkgs(new_pip_pkgs_obj)
            
            changes = {}

            if deleted_pip_pkgs:
                changes["deleted_pip_pkgs"] = deleted_pip_pkgs
            if new_pip_pkgs:
                changes["new_pip_pkgs"] = new_pip_pkgs
            if updated_pip_pkgs:
                changes["updated_pip_pkgs"] = updated_pip_pkgs

            # If any changes happens
            if changes:
                # Apply updates
                data["updated"] = datetime.utcnow
                pip_pkgs.update(**data)

                # Create a new ChangeLog entry
                change_log_entry = ChangeLogInstalledPipPackages(
                    pip_packages = pip_pkgs.id,
                    changes = changes
                )
                change_log_entry.save()
            else:
                # Apply only updated time
                pip_pkgs.update(updated=datetime.utcnow)

        except Exception as e:
            return jsonify({'error': e}), 500
        
    else:
        # CREATE If System Installed pip_pkgs not exist 
        try:
            pip_pkgs = InstalledPipPackages(**data)
            pip_pkgs.agent = agent
            pip_pkgs.save()
        except Exception as e:
            return jsonify({'error': e}), 500

    return jsonify(
        {
            'message': 'Pip packages registered successfully.',
        }
    ), 200

# Changelog Routes

# Get All Changelog Data by Pip Packages ID
@sys_pip_pkgs_bp.route('/<pip_pkgs_id>/changelog', methods=['GET'])
@auth_token_required
def get_pip_pkgs_changelog_by_pip_pkgs_id(pip_pkgs_id):
    try:
        pip_pkgs_changelog = ChangeLogInstalledPipPackages.objects(pip_packages=pip_pkgs_id)
        return [info.serialize() for info in pip_pkgs_changelog] # Serialize & Return
    except Exception as e:
        print(e)
        return jsonify({"Message":"Not Found"}), 404
##############################################################################