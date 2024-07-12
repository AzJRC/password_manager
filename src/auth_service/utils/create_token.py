import jwt
import datetime

from ..config import config
from ..view.schemas import User
from .logger import LOGGING
if LOGGING:
    from .logger import logger


def create_token(username, email):
    """
    Create a JWT token given the user's infomation.

    PARAMETERS:
    + user: [User #Schema] The user information to whom will
    provide an access or refresh token

    RETURN: [STRING] A jwt bearer token.
    """

    CURRENT_TIME = datetime.datetime.now(tz=datetime.timezone.utc)
    TIME_DELTA = 60 * int(config['JWT_EXPIRATION']) if config['JWT_EXPIRATION'] else 60 * 30

    if LOGGING:
        logger.info(f"Creating Token for User: {username}")

    user = User(username=username, email=email)

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
