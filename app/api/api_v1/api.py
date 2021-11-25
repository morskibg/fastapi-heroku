from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, addresses, contractors, contracts, itn_metas, itn_schedules

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(
    contractors.router, prefix="/contractors", tags=["contractors"])
api_router.include_router(
    addresses.router, prefix="/addresses", tags=["addresses"])
api_router.include_router(
    itn_metas.router, prefix="/itn_metas", tags=["itn_metas"])
api_router.include_router(
    itn_schedules.router, prefix="/schedules", tags=["schedules"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
