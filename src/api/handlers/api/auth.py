from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.request.auth import RegisterRequest
from api.schemas.response.base import MessageResponse
from api.usecase.auth_service import get_auth_service
from settings.db import get_db

router = APIRouter()

@router.post("/register", response_model=MessageResponse, status_code=201)
async def register(register_request: RegisterRequest, session: AsyncSession = Depends(get_db().get_session)):
    service = get_auth_service()

    await service.register(session, register_request)
    return MessageResponse(msg="success")
