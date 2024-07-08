from fastapi import FastAPI
from fastapi.testclient import TestClient
from .routes import login, register

from .utils.logger import LOGGING
if LOGGING:
    from .utils.logger import logger
    logger.info("Authentication Microservice has been Started.")


# Authentication service calling function
def run_auth_service():
    """
    Create a FastAPI web sever and authenticates user given
    the required credentials.
    It will send a HTTP response according to the client request.
    + HTTP 200 if credentials are correct + a Bearer JWT access token.
    - HTTP 40X if credentials are incorrect.
    - HTTP 500 if there is an error at querying the database.
    RETURN: An instance of the FastAPI web server (used exclusively
    for the unit tests)
    """

    server = FastAPI()

    server.include_router(login.router)
    server.include_router(register.router)

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
