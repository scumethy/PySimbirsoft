from datetime import datetime, timedelta
from jose import jwt
from argon2 import PasswordHasher
import uuid

from .config import JWT


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
    jwt_token = jwt.encode(payload, JWT["SECRET"], JWT["ALGORITHM"])
    return jwt_token


def verify_token(jwt_token):
    if jwt_token:
        try:
            payload = jwt.decode(
                jwt_token, key=JWT["SECRET"], algorithms=JWT["ALGORITHM"]
            )
        except jwt.ExpiredSignatureError:
            payload = jwt.decode(
                jwt_token,
                key=JWT["SECRET"],
                algorithms=JWT["ALGORITHM"],
                options={"verify_exp": False},
            )
            return {"user_id": payload["user_id"], "is_valid": False}

        return {"user_id": payload["user_id"], "is_valid": True}


def user_to_json(user):
    user_json = {"id": user[0], "username": user[1], "password_hash": user[2]}
    return user_json
