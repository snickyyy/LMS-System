from datetime import timedelta, datetime
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from api.enums.role import AppRole
from api.models import User
from api.repositories.user_repository import UserRepository, get_user_repository
from api.schemas.dto.session import BaseSession, RegisterSession
from api.schemas.request.auth import RegisterRequest
from api.usecase.email_service import EmailService, get_email_service
from api.usecase.session_service import SessionService, get_session_service
from settings.settings import get_settings
from utils.crypto import encrypt
from utils.hash import hash_password


class AuthService:
    def __init__(self, user_repository: UserRepository, session_service: SessionService, email_service: EmailService):
        self.user_repository = user_repository
        self.session_service = session_service
        self.email_service = email_service

    async def register(self, session:AsyncSession, request: RegisterRequest):
        user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=str(request.email),
            password=hash_password(request.password),
            role=AppRole.ANONYMOUS,
        )
        await self.user_repository.create(session, user)

        user_dto = user.to_dto()
        register_session_struct = RegisterSession(
            user_dto=user_dto
        )
        session_struct = BaseSession(
            prefix=get_settings().REDIS.PREFIXES.AUTHORIZATION,
            type=get_settings().REDIS.PREFIXES.AUTHORIZATION,
            payload=encrypt(register_session_struct.model_dump_json()),
            exp=int((datetime.now() + timedelta(seconds=get_settings().AUTH.REGISTER_EXPIRE_SEC)).timestamp())
        )

        session_id = await self.session_service.create_session(session_struct)
        await self.email_service.send_register_email(
            to=user.email,
            token=session_id,
        )

@lru_cache
def get_auth_service() -> AuthService:
    user_repository = get_user_repository()
    session_service = get_session_service()
    email_service = get_email_service()
    return AuthService(user_repository, session_service, email_service)
