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

    json_data = await request.json()
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.post(
        f"{MS_URLS['AUTH_SERVICE_URL']}/register",
        headers=headers,
        json=json_data
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()


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
