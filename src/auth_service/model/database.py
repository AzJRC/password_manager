import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger

# Configuration parameters
"""
Configuration parameters provided by system environment variables. There are
default values in case those envs were not initialized.

+ MYSQL_USER: [STRING] The user that can access the MySQL database for authentication.
+ MYSQL_PASSWORD: [STRING] The password for MYSQL_USER.
+ MYSQL_HOST: [STRING] IP, hostname, or domain of the device where the database is allocated.
+ MYSQL_PORT: [STRING] Port atwhich MySQL.service is running.
+ MYSQL_DB: [STRING] Database where user's information will be stored..
"""
load_dotenv()
config = {
        'MYSQL_USER': os.getenv('MYSQL_USER'),
        'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'MYSQL_HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'MYSQL_PORT': os.getenv('MYSQL_PORT', '3306'),
        'MYSQL_DB': os.getenv('MYSQL_DB'),
}


# SQLAlchemy parameters
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{config['MYSQL_USER']}:{config['MYSQL_PASSWORD']}@{config['MYSQL_HOST']}:{config['MYSQL_PORT']}/{config['MYSQL_DB']}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if LOGGING:
    logger.info("Database Connection Parameters Created")
