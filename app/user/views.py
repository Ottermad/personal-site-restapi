"""Views file."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

from internal.errors import HTTPException, MissingKeyError, NoJSONError
from internal.services import USER_SERVICE
import requests

from app.utils import forward_request_to_service


user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route("/user", methods=("POST",))
@jwt_required
def create_or_list_user():
    """Create or list user."""
    return forward_request_to_service(request, USER_SERVICE, "/user")


@user_blueprint.route("/auth", methods=("POST",))
def create_token():
    """Route to create a JWT token."""
    json_data = request.get_json()
    if json_data is None:
        raise NoJSONError()

    expected_keys = ["email", "password"]
    for key in expected_keys:
        if key not in json_data.keys():
            raise MissingKeyError(key)

    email = json_data['email']
    password = json_data['password']

    # Check email and password
    response = requests.post(
        USER_SERVICE.host + '/authenticate',
        json={'email': email, 'password': password},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise HTTPException(
            response.status_code,
            response.json()
        )

    user_id = response.json()['pk']
    token = {'access_token': create_access_token(identity=user_id), 'user_id': user_id}

    return jsonify(token)
