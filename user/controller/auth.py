from flask_jwt_extended import create_access_token
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from pymongo import MongoClient
import hashlib
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["mydatabase"]
users_collection = db["users"]

auth_controller = Blueprint('auth_controller', __name__)


@auth_controller.route('/login', methods=['POST'])
@cross_origin()
def login():
    try:
        user_data = request.get_json()

        username = user_data.get('username')
        password = user_data.get('password')

        if not username or not password:
            return jsonify({'msg': 'Username or password is missing'}), 400

        # Hash the password to compare with the stored hash
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # Check if the user exists
        user = users_collection.find_one({"username": username})

        if not user:
            return jsonify({'msg': 'User not found'}), 404

        # Check if the password matches
        if user["password"] == hashed_password:
            # Creating access token
            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'msg': 'Wrong password'}), 401
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Something went wrong'}), 500


@auth_controller.route('/register', methods=['POST'])
def register():
    try:
        new_user_data = request.get_json()

        username = new_user_data.get('username')
        password = new_user_data.get('password')

        if not username or not password:
            return jsonify({'msg': 'Username or password is missing'}), 400

        # Hash the password before storing it in the database
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # Check if the user already exists
        existing_user = users_collection.find_one({"username": username})

        if existing_user:
            return jsonify({'msg': 'Username already exists'}), 409

        # Create a new user
        new_user = {
            'username': username,
            'password': hashed_password
        }

        users_collection.insert_one(new_user)

        return jsonify({'msg': 'User created successfully'}), 201
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Something went wrong'}), 500
