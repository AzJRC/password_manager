import jwt
import datetime
import os
from dotenv import load_dotenv

from ..view.schemas import User
from .logger import LOGGING
if LOGGING:
    from .logger import logger

"""
+ JWT_SECRET: [STRING] A signature to ensure the validity of the JWT token.
+ JWT_EXPIRATION: [INT] Number of MINUTES the JWT will be acceptable.
+ JWT_ALGORITHM: [STRING] Algorithm used for signing process.
"""

load_dotenv()
config = {
    'JWT_SECRET': os.getenv('JWT_SECRET'),
    'JWT_EXPIRATION': os.getenv('JWT_EXPIRATION', 30),
    'JWT_ALGORITHM': os.getenv('JWT_ALGORITHM', 'HS256')
}


def create_token(user: User):
    """
    Create a JWT token given the user's infomation.

    PARAMETERS:
    + user: [User #Schema] The user information to whom will
    provide an access or refresh token

    RETURN: [STRING] A jwt bearer token.
    """
    if LOGGING:
        logger.info(f"Creating Token for User: {user.username}")
    CURRENT_TIME = datetime.datetime.now(tz=datetime.timezone.utc)
    TIME_DELTA = 60*int(config['JWT_EXPIRATION']) if config['JWT_EXPIRATION'] else 60*30

    jwt_payload = {
            "username": user.username,
            "expiration": (CURRENT_TIME + datetime.timedelta(seconds=TIME_DELTA)).isoformat(),
            "issued_at": (CURRENT_TIME).isoformat()
            }
    jwt_token = jwt.encode(
            payload=jwt_payload,
            key=config['JWT_SECRET'],
            algorithm=config['JWT_ALGORITHM']
            )
    return jwt_token
