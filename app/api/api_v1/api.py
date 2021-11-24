from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, addresses, contractors

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    contractors.router, prefix="/contractors", tags=["contractors"])
api_router.include_router(
    addresses.router, prefix="/addresses", tags=["addresses"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
