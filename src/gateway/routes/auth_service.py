import requests
from typing import Annotated
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Request, Depends, HTTPException

from ..schemas.users import SensibleUser
from ..config import MS_URLS
from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger

router = APIRouter()


@router.post("/register")
async def auth_register(user: SensibleUser, request: Request):
    if LOGGING:
        logger.info("Auth Service Request: User Registration Action.")

    # Request
    req_json_data = await request.json()
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Calling the request
    auth_response = requests.post(
        f"{MS_URLS['AUTH_SERVICE_URL']}/register",
        headers=headers,
        json=req_json_data
    )

    # Return unsuccesfull responses
    if auth_response.status_code != 200:
        if LOGGING:
            logger.info("Auth Service Error: User registration failed.")
        return auth_response.json()

    if LOGGING:
        logger.info(f"User Registration Successfull (1/2): auth_service[{auth_response.json()}]")

    # Create user's vault
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    vault_response = requests.post(
        f"{MS_URLS['VAULT_SERVICE_URL']}/vault/create",
        headers=headers,
        json=auth_response.json()
    )

    if vault_response.status_code != 200:
        if LOGGING:
            logger.info("Vault Service Error: User's vault creation failed.")
            # (TODO) Delete user's account on vault creation failure
        return vault_response.json()

    if LOGGING:
        logger.info(f"User Registration Successfull (2/2): vault_service[{vault_response.json()}]")
    return "User has been succesfully created"


@router.post("/login")
async def auth_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request):
    if LOGGING:
        logger.info("Auth Service Request: User Loging Action.")

    username = form_data.username
    password = form_data.password
    scopes = form_data.scopes

    print(form_data, username, password)

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': username,
        'password': password,
        'scopes': scopes
    }

    response = requests.post(
        f"{MS_URLS['AUTH_SERVICE_URL']}/login",
        headers=headers,
        data=data,
        verify=False
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()
