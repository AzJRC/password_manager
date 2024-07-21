import requests
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse

from .config import MS_URLS
from .utils.logger import LOGGING
if LOGGING:
    from .utils.logger import logger

OPEN_PATHS = [
    "/openapi.json",
    "/docs",
    "/login",
    "/register"
]

async def auth_middleware(request: Request, call_next):
    
    # Skip authentication for OPEN_PATHS
    if request.url.path in OPEN_PATHS:
        if LOGGING:
            logger.info("Gateway Middleware: Open request path")
        response = await call_next(request)
        return response

    # scrape access_token cookie
    access_token = request.cookies.get("access_token")
    if not access_token:
        if LOGGING:
            logger.warning("Gateway Middleware: Request rejected, no access token found.")
        return JSONResponse(status_code=401, content="Not authenticated.")
    
    # Validate access_token
    auth_response = requests.post(
        f"{MS_URLS['AUTH_SERVICE_URL']}/validate",
        headers={"Authorization": access_token}
    )

    if auth_response.status_code != 200:
        if LOGGING:
            logger.warning("Gateway Middleware: Request rejected, not authorized by auth service.") 
        return JSONResponse(status_code=401, content="Not authorized.")

    # Forward access_token user_info to next request
    user_info = auth_response.json()
    request.state.user_info = user_info
    
    if LOGGING:
        logger.info("Gateway Middleware: Forwarding request to the appropiate route.")
    response = await call_next(request)
    return response
