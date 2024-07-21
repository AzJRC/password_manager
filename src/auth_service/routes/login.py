from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from ..config import config
from ..controller import login_controller
from ..utils.token_ops import create_token
from ..view.schemas import User
from ..utils.fastapi_security import oauth2_scheme
from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger

SECURE_VALUE = config["HTTPS_ENABLED"]


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
    user_id, username, password, email = login_controller.verify_user(given_username, given_password)

    # Create auth and refresh token
    auth_token = create_token(user_id, username, email)
    
    # Create response for website
    content = "Login successful"
    response = JSONResponse(content=content)
    
    # secure=True with HTTPS
    response.set_cookie(key="access_token", value=f"bearer {auth_token}", httponly=True, secure=SECURE_VALUE) 

    if LOGGING:
        logger.info("User %s logged in successfully. [Token: %s]", given_username, auth_token)
    return response


