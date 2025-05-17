import time
import uuid
from datetime import timedelta, datetime

from pydantic import BaseModel

import settings.settings
from api.schemas.dto.user import UserDTO


class BaseSession(BaseModel):
    session_id: uuid.UUID = uuid.uuid4()
    prefix: str
    payload: str
    exp: int

class RegisterSession(BaseModel):
    UserDTO: UserDTO
    prefix: str
    payload: str
    exp: int = int((datetime.now() + timedelta(seconds=settings.settings.get_settings().AUTH.REGISTER_EXPIRE_SEC)).timestamp())
