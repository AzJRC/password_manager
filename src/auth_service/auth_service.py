from fastapi import FastAPI
from fastapi.testclient import TestClient
from .routes import login, register, validate

from .utils.logger import LOGGING
if LOGGING:
    from .utils.logger import logger
    logger.info("Authentication Microservice has been Started.")


# Authentication service calling function
def run_auth_service():
    """
    FastAPI Web Server
    This is the entry point of the Microservice Authentication Service for the
    Password Manager. The expected way to access this application is trough the
    Microservice Gateway Service.
    This application handles everything related to user operations. The following
    options are available:
        - User registration: Registered users will be able to use the Password Manager Application.
        - User authentication: Only authenticated users will be able to access their vaults.
        - User deletion: Delete users accounts and propietary data.
    To know more about this part of the Password Manager Application, you may want to
    refer to the README file located in the same directory where this file is.
    """

    server = FastAPI()

    server.include_router(login.router)
    server.include_router(register.router)
    server.include_router(validate.router)

    return server


server = run_auth_service()


# Unit tests
def test_login():
    server = run_auth_service()
    client = TestClient(server)
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "1234"}
    )
    assert response.status_code == 200


if __name__ == "__main__":
    test_login()
