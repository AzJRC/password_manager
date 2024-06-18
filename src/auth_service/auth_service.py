import logging, json, jwt, datetime, os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi.testclient import TestClient 

# Logging for debugging
LOGGING = True
if LOGGING:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


# Configuration parameters

"""
Configuration parameters provided by system environment variables. There are
default values in case those envs were not initialized.

+ MYSQL_USER: [STRING] The user that can access the MySQL database for authentication.
+ MYSQL_PASSWORD: [STRING] The password for MYSQL_USER.
+ MYSQL_HOST: [STRING] IP, hostname, or domain of the device where the database is allocated.
+ MYSQL_PORT: [STRING] Port atwhich MySQL.service is running.
+ MYSQL_DB: [STRING] Database where user's information will be stored..

+ JWT_SECRET: [STRING] A signature to ensure the validity of the JWT token.
+ JWT_EXPIRATION: [INT] Number of MINUTES the JWT will be acceptable.
+ JWT_ALGORITHM: [STRING] Algorithm used for signing process.
"""

load_dotenv()
config = {
        'MYSQL_USER': os.getenv('MYSQL_USER'),
        'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'MYSQL_HOST': os.getenv('MYSQL_HOST', 'localhost'),
        'MYSQL_PORT': os.getenv('MYSQL_PORT', '3306'),
        'MYSQL_DB': os.getenv('MYSQL_DB'),
        'JWT_SECRET': os.getenv('JWT_SECRET', '1234abcd'),
        'JWT_EXPIRATION': os.getenv('JWT_EXPIRATION', 30),
        'JWT_ALGORITHM': os.getenv('JWT_ALGORITHM', 'HS256')
}

# Schemas

"""
This schema defines the PUBLIC information that defines a User. Private information of a user
is defines in the SensibleUser schema.
"""


class User(BaseModel):
    username: str
    email: str


"""
This schema defines PRIVATE information that defines a User.
- Subclass of the User class.
"""


class SensibleUser(User):
    password: str


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

    # SQLAlchemy parameters
    SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{config['MYSQL_USER']}:{config['MYSQL_PASSWORD']}@{config['MYSQL_HOST']}:{config['MYSQL_PORT']}/{config['MYSQL_DB']}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    # Security variables
    crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    # Functions
    def create_token(user: User):
        """
        Create a JWT token given the user's infomation.

        PARAMETERS:
        + user: [User #Schema] The user information to whom will
        provide an access or refresh token

        RETURN: [STRING] A jwt bearer token.
        """

        CURRENT_TIME = datetime.datetime.now(tz=datetime.timezone.utc)
        TIME_DELTA = 60*int(config['JWT_EXPIRATION']) if config['JWT_EXPIRATION'] else 60*30       

        jwt_payload = {
                "username": user.username,
                "expiration": (CURRENT_TIME + datetime.timedelta(seconds=TIME_DELTA)).isoformat(), 
                "issued_at": (CURRENT_TIME).isoformat()
                }
        jwt_token = jwt.encode(
                payload=jwt_payload,
                key=config['JWT_SECRET'],
                algorithm=config['JWT_ALGORITHM']
                )
        return jwt_token

    # Routes
    @server.post("/register")
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

    @server.post("/login")
    async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        given_username = form_data.username
        given_password = form_data.password

        if not given_username or not given_password:
            if LOGGING:
                logger.warning("Missing username or password for login attempt.")
            raise HTTPException(status_code=401, detail="Missing username or password")

        if LOGGING:
            logger.info("Login attempt for user: %s", given_username)

        # Verify if the user exists in the database
        with engine.connect() as con:
            if LOGGING:
                logger.info("Loging in user...")
            try:
                result = con.execute(
                        text("SELECT username, password, email FROM auth WHERE username=:username"),
                        {"username": given_username}
                        ).fetchone()
            except Exception as e:
                if LOGGING:
                    logger.error("Something went wrong (10): %s", e)
                raise HTTPException(status_code=500, detail="Something went wrong in the server")
        try: 
            password_match = crypto_context.verify(given_password, result[1])
        except Exception as e:
            if LOGGING:
                logger.error("Something went wrong (11): %s", e)
            raise HTTPException(status_code=500, detail="Something went wrong in the server")

        if not result or result[0] != given_username or not password_match: 
            if LOGGING:
                logger.warning("Username or password are not correct: %s", given_username)
            raise HTTPException(status_code=401, detail="Username or password are incorrect")

        # Create auth and refresh token
        user = User(username=result[0], email=result[2])
        auth_token = create_token(user)

        if LOGGING:
            logger.info("User %s logged in successfully. Token: %s", given_username, auth_token)
        return {"access_token": auth_token, "token_type": "bearer"}

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
