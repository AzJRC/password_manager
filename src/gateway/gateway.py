import logging, json, datetime, os, requests
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Request, Depends, HTTPException
from dotenv import load_dotenv

# Logging for debugging
LOGGING = True
if LOGGING:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

# Environment Variables
load_dotenv()

# Microservices
MS_URLS = {
    'AUTH_SERVICE_URL': os.getenv('AUTH_SERVICE_URL', 'http://localhost:8001'),
    'VAULT_SERVICE_URL': os.getenv('VAULT_SERVICE_URL', 'http://localhost:8002')
}

# Parameters
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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
    async def auth_register(request: Request):
        data = await request.json()
        if LOGGING:
            logger.info("Register request received: %s", data)
       
        # Verify request

        # Forward request
        response = requests.post(f"{MS_URLS['AUTH_SERVICE_URL']}/register", json=data)
        if response.status_code != 200:
            if LOGGING:
                logger.error("- Registration failed (10): %s", response.text)
            raise HTTPException(status_code=response.status_code, detail=response.json())

        if LOGGING:
            logger.info("Registration succesfull (11): %s", response.json())

    # form_data: Annotated[OAuth2PasswordRequestForm, Depends()]

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

    return server


server = run_gateway()


# Unit tests

def test_gateway():
    server = run_gateway()
    client = TestClient(server)
    # response = client.post(
    #        # (TODO: Test every route)
    #        )
    # assert response.status_code == 200


if __name__ == "__main__":
    test_gateway()
