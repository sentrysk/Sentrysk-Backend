#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import pymongo
from datetime import datetime
from bson import json_util, ObjectId

from Shared.configs import DB_NAME,DB_HOST,DB_PORT,DB_USERNAME,DB_PASSWORD
from Shared.validators import agent_token_required, auth_token_required
from Agents.helper_funcs import get_id_by_token
##############################################################################

# Blueprint
##############################################################################
sys_data_bp = Blueprint('system_data_blueprint', __name__)
##############################################################################

# Mongo Configs
##############################################################################
# Replace these values with your MongoDB connection details
mongo_client = pymongo.MongoClient(
    f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
)
db = mongo_client[DB_NAME]
system_data_collection  = db["system_data"]
changelog_collection    = db["changelog"]
##############################################################################


##############################################################################
def compare_and_log_changes(existing_item, new_item, parent_key="", changes={}):
    if isinstance(new_item, dict):
        for key, value in new_item.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            changes = compare_and_log_changes(existing_item.get(key, {}), value, parent_key=full_key, changes=changes)
    elif isinstance(new_item, list):
        for i, item in enumerate(new_item):
            full_key = f"{parent_key}[{i}]"
            changes = compare_and_log_changes(existing_item[i] if i < len(existing_item) else {}, item, parent_key=full_key, changes=changes)
    elif new_item != existing_item:
        changes[parent_key] = {"new_value": new_item, "previous_value": existing_item}
    return changes
##############################################################################

# Routes
##############################################################################

# Get All SysData
@sys_data_bp.route('/', methods=['GET'])
@auth_token_required
def list_all_data():
    try:
        # Fetch all documents from the collection
        all_documents = list(system_data_collection.find({}))
        
        for document in all_documents:
            del document["_id"]
            document["agent_id"] = str(document["agent_id"])
        
        return jsonify(all_documents), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500

# Get SysData by ID
@sys_data_bp.route("/<string:document_id>", methods=["GET"])
@auth_token_required
def get_sys_data_by_id(document_id):
    try:
        # Find a document by its _id
        sys_data = system_data_collection.find_one({"_id": ObjectId(document_id)})

        if sys_data:
            sys_data["_id"] = str(sys_data["_id"])
            sys_data["agent_id"] = str(sys_data["agent_id"])
            return jsonify(sys_data), 200
        else:
            return "Document not found", 404
    except Exception as e:
        return jsonify({"error":{str(e)}}),500

# Save Data
@sys_data_bp.route('/', methods=['POST'])
@agent_token_required
def register():
    # Extract the agent_token from the Authorization header
    agent_token = request.headers.get("Authorization")

    # Get Agent ID by token
    agent_id = get_id_by_token(agent_token)

    # Get Data from Request
    data = request.get_json()

    # Define the unique identifier using the agent_id
    unique_identifier = {"agent_id": agent_id}

    # Find existing document with the same identifier
    existing_document = system_data_collection.find_one(unique_identifier)

    if existing_document:
        # Document with the same identifier exists, check for changes
        changes = compare_and_log_changes(existing_document, data)

        if changes:
            # Log changes to the changelog collection
            changelog_entry = {
                "timestamp"       : datetime.utcnow(),
                "system_data_id"  : existing_document["_id"],
                "agent_id"        : agent_id,
                "changes"         : changes
            }
            changelog_collection.insert_one(changelog_entry)

            # Update the existing document with changes
            system_data_collection.update_one(unique_identifier, {"$set": data})

        # Update the existing document with changes
        system_data_collection.update_one(unique_identifier, {"$set": existing_document})
    else:
        # Document with the unique identifier doesn't exist, insert the new document
        # Insert the System Data into the System Data Collection
        data["agent_id"] = agent_id
        system_data_collection.insert_one(data)
    
    return jsonify(
        {
            'message': 'Data registered successfully.',
        }
    ), 201

# Get All Changelog Data
@sys_data_bp.route('/changelog', methods=['GET'])
@auth_token_required
def get_all_changelog_data():
    try:
        # Fetch all Changelog documents from the collection
        all_documents = list(changelog_collection.find({}))

        for document in all_documents:
            document["_id"] = str(document["_id"])
            document["system_data_id"] = str(document["system_data_id"])
            document["agent_id"] = str(document["agent_id"])
        
        return jsonify(all_documents), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 500
##############################################################################