from fastapi import FastAPI
from fastapi.testclient import TestClient
from .routes import auth_service, vault_service
from .utils.logger import LOGGING
if LOGGING:
    from .utils.logger import logger
    logger.info("Authentication Microservice has been Started.")


def run_gateway():
    """
    FastAPI Web Server
    This is the entry point of the Overall Password Manager Applciation.
    This microservice handles and forwards requests to the corresponding microservices,
    either the authentication microservice or the vault microservice.
    To know more about this part of the Password Manager Applicatin, you may want to
    refer to the README file located in the same directory where this file is.
    """

    server = FastAPI()

    server.include_router(auth_service.router)
    server.include_router(vault_service.router)

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
