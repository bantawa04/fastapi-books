from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import Config
import jwt
import uuid
import logging

passwod_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIARY = 3600


def generate_password_hash(plain_password: str) -> str:
    hash = passwod_context.hash(plain_password)
    return hash


def verify_password(plain_password: str, hash: str) -> bool:
    return passwod_context.verify(plain_password, hash)


def create_access_token(
    user_data: dict, expiary: timedelta = None, refresh_token: bool = False
):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiary if expiary is not None else timedelta(seconds=ACCESS_TOKEN_EXPIARY)
    )

    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh_token

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGO
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGO]
        )
        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
