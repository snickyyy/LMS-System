from abc import ABC


class IBaseRedisRepository(ABC):
    async def set(self, prefix: str, key: str, value: str, exat: int = 0) -> any:
        pass

    async def get(self, prefix: str, key: str) -> any:
        pass

    async def delete(self, prefix: str, key: str) -> any:
        pass

    async def exists(self, prefix: str, key: str) -> any:
        pass

    async def count(self) -> any:
        pass
