from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..controller import login_controller
from ..utils.create_token import create_token
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
            logger.warning("Missing username or password.")
        raise HTTPException(status_code=401, detail="Missing username or password.")

    if LOGGING:
        logger.info("Login attempt for user: %s", given_username)

    # Verify if the user exists in the database
    username, password, email = login_controller.verify_user(given_username, given_password)

    # Create auth and refresh token
    auth_token = create_token(username, email)

    if LOGGING:
        logger.info("User %s logged in successfully. [Token: %s]", given_username, auth_token)

    return {"access_token": auth_token, "token_type": "bearer"}
