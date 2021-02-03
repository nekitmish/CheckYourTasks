import datetime
import os

import jwt

from helpers.auth.exceptions import ReadTokenException

from dotenv import load_dotenv

load_dotenv()


secret = os.getenv('secret')


def create_token(payload: dict) -> str:
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    return jwt.encode(payload, secret, algorithm='HS256')


def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, secret, algorithms='HS256')
    except jwt.exceptions.PyJWTError:
        raise ReadTokenException



