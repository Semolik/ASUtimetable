from cashews import cache
from os import environ
cache.setup(
    f"redis://{environ.get('REDIS_HOST', 'localhost')}:{environ.get('REDIS_PORT', 6379)}",
    password=environ.get('REDIS_PASSWORD', None),
)
