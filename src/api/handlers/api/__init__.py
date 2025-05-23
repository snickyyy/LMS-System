from fastapi import APIRouter

from api.handlers.api.auth import router as auth_router

accounts_router = APIRouter(prefix="/accounts", tags=["accounts"])
accounts_router.include_router(prefix="/auth", router=auth_router)