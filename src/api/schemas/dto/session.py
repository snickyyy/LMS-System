import uuid
from datetime import timedelta, datetime

from pydantic import BaseModel

import settings.settings
from api.schemas.dto.user import UserDTO


class BaseSession(BaseModel):
    session_id: uuid.UUID = uuid.uuid4()
    prefix: str
    payload: str
    type: str
    exp: int

class RegisterSession(BaseModel):
    user_dto: UserDTO

class LoginSession(BaseModel):
    user_dto: UserDTO
