from functools import lru_cache
from uuid import uuid4

from api.errors.usecase import BadRequestError
from api.repositories.base_redis_repository import (
    BaseRedisRepository,
    get_redis_repository,
)
from api.schemas.dto.session import BaseSession
from utils.crypto import decrypt


class SessionService:
    def __init__(self, redis_repository: BaseRedisRepository):
        self.redis_repository = redis_repository

    async def create_session(self, session: BaseSession) -> uuid4:
        try:
            to_json = session.model_dump_json()
        except Exception as e:
            raise BadRequestError("Invalid session") from e
        await self.redis_repository.set(session.prefix, str(session.session_id), to_json, session.exp)
        return session.session_id

    async def get_session(self, prefix: str, session_id: str, decrypt_payload=False) -> BaseSession:
        session = await self.redis_repository.get(prefix, session_id)
        if not session:
            raise BadRequestError("Invalid session")
        try:
            session = BaseSession.model_validate_json(session)
        except Exception as e:
            raise BadRequestError("Invalid session") from e
        if decrypt_payload:
            session.payload = decrypt(session.payload)
        return session

    async def delete_session(self, prefix: str, session_id: str):
        await self.redis_repository.delete(prefix, session_id)

@lru_cache
def get_session_service() -> SessionService:
    return SessionService(get_redis_repository())
