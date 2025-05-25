import pytest

from api.errors.usecase import BadRequestError
from api.schemas.dto.session import BaseSession

from api.usecase.session_service import SessionService

from .fixtures import redis_repository


base_session = BaseSession(prefix="test", exp=3600, payload="test_payload", type="test")


@pytest.mark.asyncio
async def test_create_session_error(redis_repository):
    session_service = SessionService(redis_repository)

    with pytest.raises(BadRequestError, match="Invalid session"):
        await session_service.create_session(None)


@pytest.mark.parametrize(
    "param_session, mock_return, expected_response",
    [
        (base_session, None, base_session.session_id),
    ],
    ids=[
        "success",
    ]
)
@pytest.mark.asyncio
async def test_create_session_return(redis_repository, param_session, mock_return, expected_response):
    redis_repository.set.return_value = mock_return

    session_service = SessionService(redis_repository)

    result = await session_service.create_session(param_session)
    assert result == expected_response

