import logging, json, datetime, os, requests
from fastapi.testclient import TestClient
from fastapi import FastAPI, Request, Depends, HTTPException

# Logging for debugging
LOGGING = True
if LOGGING:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


def run_gateway():
    """
    Main entry point to the password manager application. Users
    must only have access to this interface, from which they can
    authenticate and then access their vaults.
    """
    
    server = FastAPI()

    # Routes
    # Authentiction service routes
    
    @server.post("/register")
    async def auth_register():
        pass

    @server.post("/login")
    async def auth_login():
        pass

    # Vault service routes
    
    @server.post("/vault")
    async def vault_post():
        pass

    @server.put("/vault")
    async def vault_put():
        pass

    @server.get("/vault")
    async def vault_getAll():
        pass

    @server.get("/vault/{site}")
    async def vault_getFromSite():
        pass

    @server.get("/vault/{site-url}")
    async def vault_getFromURL():
        pass


# Unit tests

def test_gateway():
    server = run_gateway()
    client = TestClient(server)
    response = client.post(
            # (TODO: Test every route)
            )
    assert response.status_code == 200


if __name__ == "__main__":
    test_gateway()
