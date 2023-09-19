""" The code defines two routes in a Flask blueprint for user-related actions, including retrieving user
    profile information and deleting a user.
    :return: The `profile` route returns a JSON response containing the user's personal information,
    notes, and todos. The `delete_user` route returns a JSON response indicating that the user has been
    deleted successfully """

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import utils

users = Blueprint("users", __name__, url_prefix='/user')


@users.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    token = utils.get_token()

    if utils.is_blacklisted(token):
        return jsonify({"message": "Unauthorized to perform action!"}), 401

    user_id = get_jwt_identity()
    user = utils.get_user(user_id)

    notes = [note.title for note in user.notes]

    return jsonify({"personal info": utils.json_encoder(user), "notes": notes})


@users.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    token = utils.get_token()

    if utils.is_blacklisted(token):
        return jsonify({"message": "Unauthorized to perform action!"}), 401

    user_id = get_jwt_identity()
    user = utils.get_user(user_id)

    from app import session

    session.delete(user)
    session.commit()

    from app import redis_client

    payload = get_jwt()
    ttl = payload['exp']

    redis_client.setex(token, ttl, user_id)

    return jsonify({"message": "User Deleted Successfully!"}), 200
