from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from ..utils.fastapi_security import crypto_context
from ..model.database import engine
from ..view.schemas import SensibleUser
from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger


def sign_in_user(given_username: str, given_email: str, given_password: str, returning: bool = True) -> dict | None:
    """
    Register an user in the application.
    This function will create an entry in the database for this user.

    PARAMETERS:
    + given_user: [STRING] username of the user.
    + given_email: [STRING] email of the user.
    + given_password: [STRING] password of the user.
    + returning: [BOOL = False] Return the inserted row.

    RETURN: [DICT | None] Return the inserted row only if returning is True.
    """

    hashed_password = crypto_context.hash(given_password)
    if LOGGING:
        logger.info("Registering user...")

    # (TODO) Define sqlalchemy models
    with engine.connect() as con:
        try:

            # Insert new user record
            con.execute(
                text("""
                    INSERT INTO users (username, email, password) VALUES (:username, :email, :password);
                """),
                {"username": given_username, "email": given_email, "password": hashed_password}
            )
            last_insert_id = con.execute(text("SELECT LAST_INSERT_ID()")).scalar()

            # Retrieve the inserted record
            if returning:
                sign_in = con.execute(
                    text("SELECT * FROM users WHERE user_id = :user_id"),
                    {"user_id": last_insert_id}
                ).fetchone()

            con.commit()
        except IntegrityError:
            if LOGGING:
                logger.warning("The username or email provided are already in use.")
            con.rollback()
            raise HTTPException(status_code=409, detail="The username or email is already in use.")
        except Exception as e:
            if LOGGING:
                logger.error("Something went wrong: %s", e)
            con.rollback()
            raise HTTPException(status_code=500, detail="Something went wrong in the server.")

        if returning:
            return sign_in._mapping
