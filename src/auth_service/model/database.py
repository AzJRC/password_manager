from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import config
from ..utils.logger import LOGGING
if LOGGING:
    from ..utils.logger import logger


# SQLAlchemy parameters
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{config['MYSQL_USER']}:{config['MYSQL_PASSWORD']}@{config['MYSQL_HOST']}:{config['MYSQL_PORT']}/{config['MYSQL_DB']}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if LOGGING:
    logger.info("Database Connection Parameters Created.")
