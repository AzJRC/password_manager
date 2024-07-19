from typing import Annotated, Any
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from .model.database import engine
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

    @server.post("/vault/create")
    def create_vault(vault_metadata: Annotated[dict, Body()]):
        metadata = vault_metadata["details"]  # (TODO) Pydantic Model

        with engine.connect() as con:
            try:
                query = text("INSERT INTO vaults (user_id) VALUES (:user_id);")
                params = {"user_id": metadata["user_id"]}
                con.execute(query, params)
                con.commit()
            except IntegrityError:
                print("Something weird that should not happen, happened")
                con.rollback()
            except Exception as e:
                print(e)
                con.rollback()

        return "vault created"

    @server.post("/vault/entry")
    def create_vault_entry(data: Annotated[dict, Body()]):
        entry_data = data["entry"]
        with engine.connect() as con:
            try:
                query = text("""INSERT INTO vault_entries (vault_id, service_name, service_url, username, email, secret)
                    VALUES (:vault_id, :service_name, :service_url, :username, :email, :secret);""")
                params = {
                    "vault_id": entry_data["vault_id"],
                    "service_name": entry_data["service_name"],
                    "service_url": entry_data["service_url"],
                    "username": entry_data["username"],
                    "email": entry_data["email"],
                    "secret": entry_data["secret"]
                }
                con.execute(query, params)
                con.commit()
            except IntegrityError:
                print("Something weird that should not happen, happened")
                con.rollback()
                return 1
            except Exception as e:
                print(e)
                con.rollback()
                return 2

        return "entry added"

    @server.get("/vault/entry")
    def get_vault_entry():
        pass

    return server


server = run_auth_service()


# Unit tests
def test_vault():
    pass


if __name__ == "__main__":
    test_vault()
