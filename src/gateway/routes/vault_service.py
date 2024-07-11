from fastapi import APIRouter

router = APIRouter()


# Vault service routes
@router.post("/vault")
async def vault_post():
    pass


@router.put("/vault")
async def vault_put():
    pass


@router.get("/vault")
async def vault_getAll():
    pass


@router.get("/vault/{site}")
async def vault_getFromSite():
    pass


@router.get("/vault/{site-url}")
async def vault_getFromURL():
    pass
