from random import choice
import aiohttp
import asyncio
from aiohttp import client_exceptions
from lxml import etree
from fastapi import HTTPException

timeout_seconds = 10
session_timeout = aiohttp.ClientTimeout(
            total=None, sock_connect=timeout_seconds, sock_read=timeout_seconds)

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

async def get_tree(url: str):
    try:
        async with aiohttp.ClientSession(timeout=session_timeout, headers=random_headers()) as session:
            response = await session.get(url)
            if 200 >= response.status > 300:
                raise HTTPException(status_code=response.status, detail="Не удалось подключиться к сайту.")
            html = await response.text()
            tree = etree.HTML(html)
            return tree
    except asyncio.exceptions.TimeoutError:
        raise HTTPException(status_code=408, detail="Не удалось подключиться к сайту.")
    except client_exceptions.ClientConnectorError:
        raise HTTPException(status_code=404, detail="Не удалось подключиться к сайту.")
    except:
        raise HTTPException(status_code=500, detail="Неизвестная ошибка.")
    
    