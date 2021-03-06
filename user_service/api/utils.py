from datetime import datetime, timedelta
from jose import jwt
from argon2 import PasswordHasher
import uuid

from user_service.config import config
import user_service.api.errors as errors


def get_unique_uuid():
    return str(uuid.uuid4())


def get_password_hash(password):
    ph = PasswordHasher()
    hash = ph.hash(password)
    return hash


def verify_password(password_hash, password):
    ph = PasswordHasher()
    try:
        ph.verify(password_hash, password)
        return True
    except:
        return False


def generate_jwt(user_id):
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(minutes=45)}
    jwt_token = jwt.encode(payload, config.jwt_secret, config.jwt_algo)
    return jwt_token


def verify_token(jwt_token):
    if jwt_token:
        try:
            payload = jwt.decode(
                jwt_token, key=config.jwt_secret, algorithms=config.jwt_algo
            )
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            raise errors.BadAuthData


def user_to_json(user):
    user_json = {"id": user[0], "username": user[1], "password_hash": user[2]}
    return user_json
