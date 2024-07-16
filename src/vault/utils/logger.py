import logging

LOGGING = True
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
if LOGGING:
    logger.warning("LOGGER ENABLED")
