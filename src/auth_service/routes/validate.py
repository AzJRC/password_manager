from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from ..config import config
from ..utils.token_ops import validate_token, validate_token_entry, validate_token_info
from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger

SECURE_VALUE = config["HTTPS_ENABLED"]


router = APIRouter()

@router.post("/validate")
async def login(request: Request):
    access_token = request.headers.get("Authorization")
    
    try:
        jwt_token = access_token.split(" ")[1]
    except:
        if LOGGING:
            logger.warning("Not properly formated access_token.")
        raise HTTPException(status_code=401, detail="Invalid access_token.")

    if jwt_token is None:
        raise HTTPExeption(status_code=401, detail="Invalid access_token.")
    
    # Validate token
    payload = await validate_token(jwt_token)
    if not payload:
        if LOGGING:
            logger.warning("JWT has no payload.")
        raise HTTPException(status_code=401, detail="Invalid access_token.")

    # Validate token in database
    valid_token_entry = await validate_token_entry(jwt_token)  # (TODO)
    if not valid_token_entry:
        if LOGGING:
            logger.warning("JWT not found in database.")
        raise HTTPException(status_code=401, detail="Invalid access token.")

    # Validate token information
    valid_user_info = await validate_token_info(payload)  # (TODO)
    if not valid_user_info:
        if LOGGING:
            logger.warning("JWT contains invalid information.")
        raise HTTPException(status_code=401, detail="Invalid access token.")

    return payload
