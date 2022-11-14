"""Services module."""

from aioredis import Redis


class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def GetCache(self, key) -> str:
        return await self._redis.get(key, encoding="utf-8")

    async def SetCache(self, key, value, time=60*10) -> str:
        await self._redis.set(key, value, expire=time)
