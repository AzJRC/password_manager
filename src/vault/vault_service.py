from fastapi import FastAPI
from fastapi.testclient import TestClient

from .utils.logger import LOGGING
if LOGGING:
    from .utils.logger import logger
    logger.info("Vault Microservice has been Started.")


# Authentication service calling function
def run_auth_service():
    """
    FastAPI Web Server
    """

    server = FastAPI()

    # server.include_router(login.router)
    # server.include_router(register.router)
    
    @server.post("/vault")
    def store():
        pass

    return server


server = run_auth_service()


# Unit tests
def test_vault():
    pass


if __name__ == "__main__":
    test_vault()
