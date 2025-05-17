from pydantic import BaseModel

from api.enums.role import AppRole


class UserDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: str = AppRole.ANONYMOUS.name
    description: str | None = None
    image: str | None = None
