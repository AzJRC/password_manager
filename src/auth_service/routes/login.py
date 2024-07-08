from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text

from ..utils.passlib_context import crypto_context
from ..utils.create_token import create_token
from ..model.database import engine
from ..view.schemas import User
from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger

router = APIRouter()


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    given_username = form_data.username
    given_password = form_data.password

    if not given_username or not given_password:
        if LOGGING:
            logger.warning("Missing username or password for login attempt.")
        raise HTTPException(status_code=401, detail="Missing username or password")

    if LOGGING:
        logger.info("Login attempt for user: %s", given_username)

    # Verify if the user exists in the database
    with engine.connect() as con:
        if LOGGING:
            logger.info("Loging in user...")
        try:
            result = con.execute(
                    text("SELECT username, password, email FROM auth WHERE username=:username"),
                    {"username": given_username}
                    ).fetchone()
        except Exception as e:
            if LOGGING:
                logger.error("Something went wrong (10): %s", e)
            raise HTTPException(status_code=500, detail="Something went wrong in the server")
    try:
        password_match = crypto_context.verify(given_password, result[1])
    except Exception as e:
        if LOGGING:
            logger.error("Something went wrong (11): %s", e)
        raise HTTPException(status_code=500, detail="Something went wrong in the server")

    if not result or result[0] != given_username or not password_match:
        if LOGGING:
            logger.warning("Username or password are not correct: %s", given_username)
        raise HTTPException(status_code=401, detail="Username or password are incorrect")

    # Create auth and refresh token
    user = User(username=result[0], email=result[2])
    auth_token = create_token(user)

    if LOGGING:
        logger.info("User %s logged in successfully. Token: %s", given_username, auth_token)
    return {"access_token": auth_token, "token_type": "bearer"}
