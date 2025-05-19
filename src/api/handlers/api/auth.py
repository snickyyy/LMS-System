from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.request.auth import RegisterRequest
from api.schemas.response.base import MessageResponse
from api.usecase.auth_service import get_auth_service
from settings.db import get_db
from settings.settings import get_settings

router = APIRouter()

@router.post("/register", response_model=MessageResponse, status_code=201)
async def register(register_request: RegisterRequest, session: AsyncSession = Depends(get_db().get_session)):
    service = get_auth_service()

    await service.register(session, register_request)
    return MessageResponse(msg="success")

@router.get("/activate-account/{token}", response_model=MessageResponse, status_code=200)
async def activate_account(response: Response, token: str, session: AsyncSession = Depends(get_db().get_session)):
    service = get_auth_service()

    session = await service.confirm_account(session, token)
    response.set_cookie("sessionID", session, get_settings().AUTH.LOGIN_EXPIRE_SEC, secure=True, httponly=True)
    return MessageResponse(msg="success")
