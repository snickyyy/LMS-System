from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer

from api.schemas.request.auth import RegisterRequest, LoginRequest
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

@router.post("/login", response_model=MessageResponse, status_code=200)
async def login(response: Response, login_request: LoginRequest, session: AsyncSession = Depends(get_db().get_session)):
    service = get_auth_service()

    session = await service.login(session, login_request)
    response.set_cookie("sessionID", session, get_settings().AUTH.LOGIN_EXPIRE_SEC, secure=True, httponly=True)
    return MessageResponse(msg="success")

@router.delete("/logout", response_model=MessageResponse, status_code=200)
async def logout(request: Request, response: Response):
    service = get_auth_service()

    await service.logout(request.cookies.get("sessionID"))
    response.delete_cookie("sessionID")
    return MessageResponse(msg="success")
