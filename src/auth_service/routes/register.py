from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from ..utils.passlib_context import crypto_context
from ..model.database import engine
from ..view.schemas import SensibleUser
from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger

router = APIRouter()


@router.post("/register")
async def register(form_data: SensibleUser):
    given_username = form_data.username
    given_password = form_data.password
    given_email = form_data.email

    if not given_username or not given_password or not given_email:
        if LOGGING:
            logger.warning("Missing username, password or email for register attempt.")
        raise HTTPException(status_code=401, detail="Missing username, password or email")

    if LOGGING:
        logger.info("Register attempt for user: %s - %s", given_username, given_email)

    # (TODO: Verify email address? )

    # Hash password (TODO: implement salting)
    hashed_password = crypto_context.hash(given_password)

    # Store username in database
    with engine.connect() as con:
        if LOGGING:
            logger.info("Registering user...")
        try:
            con.execute(
                text("""INSERT INTO auth (username, email, password) VALUES (:username, :email,
                    :password)"""),
                {"username": given_username, "email": given_email, "password": hashed_password}
            )
        except IntegrityError:
            if LOGGING:
                logger.warning("The username or email provided are already in use.")

            con.rollback()
            raise HTTPException(status_code=400, detail="The username or email is already in use")
        except Exception as e:
            if LOGGING:
                logger.error("Something went wrong (20): %s", e)
            con.rollback()
            raise HTTPException(status_code=500, detail="Something went wrong in the server")

        con.commit()

    if LOGGING:
        logger.info("User %s registered in successfully.", given_username)
    return {"message": "Success"}
