import aiohttp
import asyncio
from aiohttp import client_exceptions
from lxml import etree
from fastapi import HTTPException

timeout_seconds = 10
session_timeout = aiohttp.ClientTimeout(
            total=None, sock_connect=timeout_seconds, sock_read=timeout_seconds)


async def get_tree(url: str):
    try:
        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            response = await session.get(url)
            if response.status != 200:
                return response.status
            html = await response.text()
            tree = etree.HTML(html)
            return tree
    except asyncio.exceptions.TimeoutError:
        raise HTTPException(status_code=408, detail="Не удалось подключиться к сайту.")
    except client_exceptions.ClientConnectorError:
        raise HTTPException(status_code=404, detail="Не удалось подключиться к сайту.")
    except:
        raise HTTPException(status_code=500, detail="Неизвестная ошибка.")
    
    