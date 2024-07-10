from typing import Tuple
from sqlalchemy import text
from fastapi import HTTPException

from ..model.database import engine
from ..utils.fastapi_security import crypto_context
from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger


# (TODO) Verify user also with email
def verify_user(given_username: str, given_password: str) -> tuple[str]:
    """
    Verify credentials of a user.

    PARAMETERS:
    + given_username: [STRING] username of the user to verify.
    + given_password: [STRING] password of the user to verify.

    RETURN: [TUPLE] A tuple containing the username, password, and email of the user.
    """

    if LOGGING:
        logger.info("Verifying user...")

    # Get user using given_username from the database
    with engine.connect() as con:
        try:
            verified_user = con.execute(
                text("SELECT username, password, email FROM auth WHERE username=:username"),
                {"username": given_username}
            ).fetchone()
        except Exception as e:
            if LOGGING:
                logger.error("Something went wrong: %s", e)
            raise HTTPException(status_code=500, detail="Something went wrong in the server.")
    if LOGGING:
        logger.info("Verification completed.")

    username = verified_user[0]
    password = verified_user[1]
    email = verified_user[2]

    # Compare user's password with user's given_password
    try:
        password_match = crypto_context.verify(given_password, password)
    except Exception as e:
        if LOGGING:
            logger.error("Something went wrong: %s", e)
        raise HTTPException(status_code=500, detail="Something went wrong in the server.")

    # Verify that the user provided the correct password
    if not username or not password_match:
        if LOGGING:
            logger.warning("Username or password are not correct: %s", given_username)
        raise HTTPException(status_code=401, detail="Username or password are incorrect.")

    return (username, password, email)
