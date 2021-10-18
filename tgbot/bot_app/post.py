import aiohttp
import asyncio
from .credentials import API_URI_CREATE
async def post(**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URI_CREATE, data=kwargs) as resp:
            print(resp.status)
            print(await resp.text())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(post())
