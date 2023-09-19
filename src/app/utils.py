from app import models
from flask import request
from sqlalchemy import select
import bcrypt


def json_encoder(obj):
    if isinstance(obj, models.User):
        return {"username": obj.username, "email": obj.email}

    elif isinstance(obj, models.Note):
        return {"id": obj.id, "title": obj.title, "content": obj.content}

    else:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_blacklisted(token):
    from app import redis_client

    if redis_client.exists(token):
        return True

    return False


def get_user(user_id):
    from app import session

    query = select(models.User).where(models.User.id == user_id)
    record = session.execute(query).first()

    if not record:
        return None

    user = record[0]

    return user


def get_token():
    header = request.headers['Authorization']
    token = header.split(' ')[1]

    return str(token)
