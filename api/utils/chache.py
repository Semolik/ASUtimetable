from fastapi import Depends
from dependency_injector.wiring import Provide
from datetime import datetime, timedelta
import json
from api.containers import Container
from api.services import Service
from api.config import DATETIME_FORMAT
from api.utils.errors import ErrorMessage
from api.utils.messages import GetMessage, messages
from api.utils.parce import GetPage
from api.utils.time import last_updated_timedelta_to_text


async def GetChacheRequest(key, function=GetPage, service: Service = Depends(Provide[Container.service]), post_processing_function=None, chache_hours=5, **kwargs):
    cache_data = await service.GetCache(key)
    async def items_result(items):
        if post_processing_function:
            return await post_processing_function(items)
        return items
    if cache_data:
        items_cache = json.loads(cache_data)
        caching_date = datetime.strptime(
            items_cache.get('date'), DATETIME_FORMAT)
        now = datetime.now()
        last_updated = now - caching_date
        if last_updated > timedelta(hours=chache_hours):
            items = await function(key=key, **kwargs)
            if isinstance(items, int):
                del items_cache['date']
                items_cache['last_updated'] = last_updated_timedelta_to_text(
                    last_updated)
                items_cache['message'] = f"{GetMessage(items)} {messages.get('last')}"
                return await items_result(items_cache)
        else:
            del items_cache['date']
            items_cache['last_updated'] = last_updated_timedelta_to_text(
                last_updated)
            return await items_result(items_cache)
    else:
        items = await function(key=key, **kwargs)
        if isinstance(items, int):
            return ErrorMessage(message=GetMessage(items), status_code=items)
    items['last_updated'] = 'сейчас'
    return await items_result(items)
