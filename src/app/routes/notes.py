""" The code defines a Flask blueprint for managing notes, including routes for getting all notes,
    getting a specific note, creating a note, updating a note, and deleting a note.
    :return: The code is returning JSON responses for various API endpoints. The responses include
    messages, data, and status codes. """

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from app import models, schemas, utils
from pydantic import ValidationError

notes = Blueprint("notes", __name__, url_prefix='/notes')


@notes.route('', methods=['GET'])
@jwt_required()
def get_all_notes():
    token = utils.get_token()

    if utils.is_blacklisted(token):
        return jsonify({"message": "Unauthorized to perform action!"}), 401

    user_id = get_jwt_identity()
    user = utils.get_user(user_id)

    if user is None:
        return jsonify({"message": "User Not Found!"}), 404

    notes = list()

    for note in user.notes:
        notes.append(utils.json_encoder(note))

    return jsonify({"username": user.username, "notes": notes}), 200


@notes.route('/<title>', methods=['GET'])
@jwt_required()
def get_note(title):
    token = utils.get_token()

    if utils.is_blacklisted(token):
        return jsonify({"message": "Unauthorized to perform action!"}), 401

    user_id = get_jwt_identity()
    user = utils.get_user(user_id)

    if user is None:
        return jsonify({"message": "User Not Found!"}), 404

    for note in user.notes:
        if note.title == title:
            return utils.json_encoder(note), 200

    return jsonify({"message": "Record Not Found!"}), 404


@notes.route('/create', methods=['POST'])
@jwt_required()
def create_note():
    token = utils.get_token()

    if utils.is_blacklisted(token):
        return jsonify({"message": "Unauthorized to perform action!"}), 401

    try:
        valid_data = schemas.Note(**request.json)

    except ValidationError as error:
        return jsonify({"Error": str(error)}), 400

    user_id = get_jwt_identity()

    note = models.Note(title=valid_data.title,
                       content=valid_data.content, user_id=user_id)

    from app import session

    try:
        session.add(note)
        session.commit()

        return jsonify({"message": "Note created Successfully", "note": utils.json_encoder(note)}), 200

    except IntegrityError:
        session.rollback()
        return {"error": "Integrity Error", "message": "The Operation couldn't be completed due to\
                 database integrity error. Please check your input and try again."}, 400


@notes.route('/update/<title>', methods=['PUT'])
@jwt_required()
def update_notes(title):
    token = utils.get_token()

    if utils.is_blacklisted(token):
        return jsonify({"message": "Unauthorized to perform action!"}), 401

    data = request.json
    user_id = get_jwt_identity()
    user = utils.get_user(user_id)

    from app import session

    for note in user.notes:
        if note.title == title:
            try:
                note.title = data['new_title']
                note.content = data['new_content']
                session.commit()

                return jsonify({"message": "Record updated Successfully", "new note": utils.json_encoder(note)}), 200

            except IntegrityError:
                session.rollback()
                return {"error": "Integrity Error", "message": "The Operation couldn't be completed due to\
                        database integrity error. Please check your input and try again."}, 400

    return jsonify({"message": "Record Not Found!"}), 404


@notes.route('/delete/<title>', methods=['DELETE'])
@jwt_required()
def delete_note(title):
    token = utils.get_token()

    if utils.is_blacklisted(token):
        return jsonify({"message": "Unauthorized to perform action!"}), 401

    user_id = get_jwt_identity()
    user = utils.get_user(user_id)

    if user is None:
        return jsonify({"message": "User Not Found!"}), 404

    from app import session

    for note in user.notes:
        if note.title == title:
            session.delete(note)
            session.commit()

            return jsonify({"message": "Note Deleted Sucessfully!"}), 200

    return jsonify({"mesasge": "Record Not Found!"}), 404
