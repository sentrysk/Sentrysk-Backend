#!/usr/bin/env python3

# Libraries
##############################################################################
from flask import Blueprint, request, jsonify
import bcrypt
import jwt
from datetime import datetime,timedelta
from marshmallow import  ValidationError

from .models import User
from Session.models import Session
from .schema import RegisterSchema,LoginSchema,UpdatePasswordSchema
from Shared.configs import SECRET_KEY,JWT_ALG
from Shared.validators import auth_token_required
from .helper_funcs import get_email_by_token
##############################################################################

# Blueprint
##############################################################################
users_bp = Blueprint('users_blueprint', __name__)
##############################################################################

# Routes
##############################################################################

# Register Route
@users_bp.route('/register', methods=['POST'])
def register_user():
    try:
        # Load and validate the JSON request using the schema
        data = RegisterSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400

    # Get Email & Password from request data
    name        = data.get('name')
    lastname    = data.get('lastname')
    email       = data.get('email')
    password    = data.get('password')

    # Check if User already exist
    existing_user = User.objects(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already registered.'}), 409

    # Generate password hash
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Register User
    user = User(
        name     = name,
        lastname = lastname,
        email    = email, 
        password = hashed_password
    )
    user.save()

    return jsonify({
        'message': 'User registered successfully.',
        'user': user.safe_serialize()
    }), 201

# Login Route
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        # Load and validate the JSON request using the schema
        data = LoginSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400

    # Get Email & Password from request data
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = User.objects(email=email).first()

    # If User exist & Password matches
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        # Expire previous session
        prev_session = Session.objects(email=email,is_expired=False).first()
        # If Previous session exist -> Expire
        if prev_session:
            prev_session.is_expired = True
            prev_session.expire_date = datetime.utcnow()
            prev_session.save()

        # Generate a token for the user session
        token = jwt.encode(
            {
                'email': email,
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            SECRET_KEY,     # Secret Key
            JWT_ALG         # JWT Algorithm
        )

        # Create a Session for this User
        session = Session(
            email=email, 
            token=token
        )
        session.save()

        return jsonify(
            {
                'message': 'Login successful.',
                'token': token,
                'token_expiry_date': datetime.utcnow() + timedelta(hours=24)
            }
        ), 200

    return jsonify({'message': 'Invalid credentials.'}), 401

# Logout Route
@users_bp.route('/logout', methods=['POST'])
@auth_token_required
def logout():
    # Get Session if is not expired
    session = Session.objects(
        token       =  request.headers.get('Authorization'), 
        is_expired  =  False
    ).first()

    if session:
        session.is_expired = True
        session.save()
        return jsonify({'message': 'Logout successful.'}), 200
    
    return jsonify({'message': 'Token is invalid'}), 498

# Get User by ID
@users_bp.route('/<id>', methods=['GET'])
@auth_token_required
def get_user_by_id(id):
    try:
        user = User.objects(id=id).first().safe_serialize()
        return jsonify(user)
    except Exception as e:
        return jsonify({"error":str(e)}), 500

# Get All Users
@users_bp.route('/', methods=['GET'])
@auth_token_required
def get_users():
    try:
        users = User.objects()
        return [user.safe_serialize() for user in users] # Serialize & Return
    except Exception as e:
        return jsonify({"error":str(e)}), 500

# Get User Details by Token
@users_bp.route('/details', methods=['GET'])
@auth_token_required
def get_user_details_by_token():
    try:
        # Get JWT Token by Authorization Header
        jwt_token = request.headers.get('Authorization')
        # Get Email by Token
        email = get_email_by_token(jwt_token)
        # Get User object by Email and Safe Serialize
        user = User.objects(email=email).first().safe_serialize()
        return jsonify(user)
    except Exception as e:
        return jsonify({"error":str(e)}), 500
    
# Update Current User Password
@users_bp.route('/updatepass', methods=['POST'])
@auth_token_required
def update_current_user_password():
    try:
        # Load and validate the JSON request using the schema
        data = UpdatePasswordSchema().load(request.json)
    except ValidationError as e:
        # Return validation errors as a JSON response with a 400 status code
        return jsonify({'error': e.messages}), 400

    try:
        # Get JWT Token by Authorization Header
        jwt_token = request.headers.get('Authorization')
        # Get Email by Token
        email = get_email_by_token(jwt_token)
    except Exception as e:
        return jsonify({'error': e.messages}), 404

    try:
        # Get User object by Email and Safe Serialize
        user = User.objects(email=email).first()
    except Exception as e:
        return jsonify({"error":"User not found"})
    

    current_password    = data.get('current_password')
    new_password        = data.get('new_password')
    new_password_repeat = data.get('new_password_repeat')

    if new_password == new_password_repeat:
        # If Current Password matches
        if bcrypt.checkpw(current_password.encode('utf-8'), user.password):
            # Generate password hash from new_password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            # Save Updated Password
            user.password =  hashed_password  
            user.save()
            return jsonify({'message':'Password updated successfully'})
        else:
            return jsonify({'error':'Current Password not match'})
    else:
        return jsonify({'error':'Password and Repeat not match'})
        

##############################################################################