"""Example usage of pytraccar."""
import asyncio
import aiohttp
from pytraccar.api import API

LOOP = asyncio.get_event_loop()


async def test():
    """Example usage of pytraccar."""
    async with aiohttp.ClientSession() as session:
        data = API(LOOP, session)
        print(data.test)

LOOP.run_until_complete(test())
