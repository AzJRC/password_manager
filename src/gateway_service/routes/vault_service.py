from typing import Annotated, Optional
import requests
from fastapi import APIRouter, Depends, Request, Body
from pydantic import BaseModel

from ..config import MS_URLS
from .auth_service import auth_login
from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger

router = APIRouter()


class VaultEntrySchema(BaseModel):
    vault_id: int
    service_name: str
    service_url: str
    username: Optional[str] = None
    email: Optional[str] = None
    secret: str


# Vault service routes
@router.post("/vault")
async def add_vault_entry(access_token: Annotated[str, Body()], entry: VaultEntrySchema, request: Request):

    if LOGGING:
        logger.info("Vault Service Request: Adding entry to database.")

    # Request
    req_json_data = await request.json()
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Validate access_token (TODO)

    # Calling the request
    vault_response = requests.post(
        f"{MS_URLS['VAULT_SERVICE_URL']}/vault/entry",
        headers=headers,
        json=req_json_data
    )

    # Return unsuccessfull responses
    if vault_response.status_code != 200:
        if LOGGING:
            logger.info("Vault Service Error: Vault entry creation error.")
        return vault_response.json()

    if LOGGING:
        logger.info("Vault Service Sucess: Vault entry was succesfully added to the database.")
    return vault_response.json()


@router.put("/vault")
async def modify_vault_entry(token: Annotated[str, Depends(auth_login)]):
    pass


@router.get("/vault")
async def get_all_vault_entries(request: Request):
    user_info = request.state.user_info
    
    headers = {
        'accept': 'application/json',
    }
    
    # get_vault_id with user_info.user_id
    vault_id = requests.get(
        f"{MS_URLS['VAULT_SERVICE_URL']}/vault/get_vault?user_id={user_info['user_id']}",
        headers=headers
    )
    
    vault_id=4  # (TODO TMP)

    # request all vault entries
    vault_response = requests.get(
        f"{MS_URLS['VAULT_SERVICE_URL']}/vault/entry?vault_id={vault_id}",
        headers=headers
    )

    return vault_response.json()


@router.get("/vault/{site}")
async def get_site_vault_entry(token: Annotated[str, Depends(auth_login)]):
    pass


@router.get("/vault/{site-url}")
async def get_url_vault_entry(token: Annotated[str, Depends(auth_login)]):
    pass
