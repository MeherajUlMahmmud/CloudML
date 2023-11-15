from flask_jwt_extended import create_access_token
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from pymongo import MongoClient
import hashlib
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["mydatabase"]
users_collection = db["users"]

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/list', methods=['get'])
def get_users():
    try:
        users = users_collection.find(
            {
                "$or": [
                    {"role": "user"},
                    {"role": "admin"}
                ]
            }, {"_id": 0, "password": 0, "templates": 0}
        )
        users_list = []
        for user in users:
            users_list.append(user)
        return jsonify(users_list), 200
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Something went wrong'}), 500


@user_controller.route('/<username>', methods=['get'])
def get_user(username):
    try:
        user = users_collection.find_one(
            {"username": username},
            {"_id": 0, "password": 0, "templates": 0})
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        return jsonify(user), 200
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Something went wrong'}), 500
