""" The code defines routes for user authentication including signup, login, and logout using Flask and
    SQLAlchemy.
    :return: The code is returning JSON responses for different routes """

from flask import Blueprint, request, jsonify
from app import schemas, models, utils
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from datetime import timedelta
from bcrypt import checkpw
from pydantic import ValidationError


auth = Blueprint("auth", __name__, url_prefix='/auth')


@auth.route('/signup', methods=['POST'])
def signup():
    try:
        valid_data = schemas.SignUp(**request.json)

    except ValidationError as error:
        return jsonify({"Error": str(error)}), 400

    user = models.User(username=valid_data.username,
                       email=valid_data.email, password=utils.hash(valid_data.password).decode('utf-8'))

    from app import session

    try:
        session.add(user)
        session.commit()

    except IntegrityError:
        session.rollback()
        return {"error": "Integrity Error", "message": "This email is already in use. Try a different one"}, 409

    return jsonify({"message": "User created Successfully", "info": utils.json_encoder(user)}), 200


@auth.route('/login', methods=['POST'])
def login():
    try:
        data = schemas.Login(**request.json)

    except ValidationError as error:
        return jsonify({"Error": str(error)}), 400

    from app import session

    query = select(models.User).where(models.User.email == data.email)
    record = session.execute(query).first()

    if not record:
        return jsonify({"message": "Wrong Credentials!"}), 401

    user = record[0]

    if checkpw(data.password.encode('utf-8'), user.password.encode('utf-8')):
        token = create_access_token(
            identity=user.id, expires_delta=timedelta(minutes=30))

        return {"token": token}, 200

    return jsonify({"message": "Wrong Credentials!"}), 401


@auth.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    token = utils.get_token()

    if utils.is_blacklisted(token):
        return jsonify({"message": "Unauthorized to perform action!"}), 401

    user_id = get_jwt_identity()
    payload = get_jwt()

    from app import redis_client

    ttl = payload['exp']

    redis_client.setex(token, ttl, user_id)

    return jsonify({"message": "Logged out Successfully!"}), 200
