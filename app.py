from flask import Flask
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import hashlib
from flask import Flask, request, jsonify
from config import JWT_SECRET_KEY, MONGO_URI, UPLOAD_FOLDER
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import datetime
import hashlib
import urllib

from user.controller.auth import auth_controller
from user.controller.user import user_controller

app = Flask(__name__)
cors = CORS(app)
jwt = JWTManager(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 16MB

client = MongoClient(MONGO_URI)
db = client["mydatabase"]
users_collection = db["users"]
templates_collection = db["templates"]


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return 'Hello, World!'


app.register_blueprint(auth_controller, url_prefix='/api/v1/auth')
app.register_blueprint(user_controller, url_prefix='/api/v1/user')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
