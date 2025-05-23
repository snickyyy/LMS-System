from sqlalchemy import String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from api.enums.role import AppRole
from api.models.base import BaseModel
from api.schemas.dto.user import UserDTO


class User(BaseModel):
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[AppRole] = mapped_column(SqlEnum(AppRole, name='app_role'), nullable=False, default=AppRole.ANONYMOUS)
    balance: Mapped[int] = mapped_column(nullable=False, default=0)
    image: Mapped[str] = mapped_column(String(255), nullable=True)

    def to_dto(self) -> UserDTO:
        return UserDTO(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            description=self.description,
            role=self.role,
            image=self.image
        )
