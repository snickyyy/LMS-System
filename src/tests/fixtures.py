from unittest.mock import AsyncMock

import pytest

from api.interfaces.redis_repository import IBaseRedisRepository


@pytest.fixture
def redis_repository():
    return AsyncMock(spec=IBaseRedisRepository)
