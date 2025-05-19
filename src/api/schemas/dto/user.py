from pydantic import BaseModel, EmailStr

from api.enums.role import AppRole


class UserDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: AppRole = AppRole.ANONYMOUS
    description: str | None = None
    image: str | None = None

class UpdateUserDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: AppRole | None = None
    description: str | None = None
    image: str | None = None
