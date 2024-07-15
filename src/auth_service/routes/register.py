from fastapi import APIRouter, HTTPException
from ..controller import register_controller

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
        raise HTTPException(status_code=401, detail="Missing username, password, or email.")

    if LOGGING:
        logger.info("Register attempt for user: %s - %s", given_username, given_email)

    # (TODO: Verify email address)

    # sign in user
    user_registration_entry = register_controller.sign_in_user(given_username, given_email, given_password)

    if LOGGING:
        logger.info("User %s registered in successfully.", given_username)

    return {"message": "Success", "details": user_registration_entry}
