from starlette.requests import Request

from api.enums.role import AppRole
from api.schemas.dto.user import UserDTO
from api.usecase.session_service import get_session_service
from settings.settings import get_settings


async def auth_middleware(request: Request, next: callable):
    session_service = get_session_service()

    session = request.cookies.get("sessionID")

    anonymous_user = UserDTO(
        id=0,
        first_name="",
        last_name="",
        email="anonymous@ocg.dot",
    )

    if session:
        try:
            user_session = await session_service.get_session(get_settings().REDIS.PREFIXES.LOGIN, session, decrypt_payload=True)
            user = UserDTO.model_validate_json(user_session.payload)

            if user.role.value <= AppRole.ANONYMOUS.value:
                request.state.user = anonymous_user
            else:
                request.state.user = user

        except Exception as e:
            request.state.user = anonymous_user
    else:
        request.state.user = anonymous_user

    response = await next(request)
    return response
