"""Example usage of pytraccar."""
import asyncio
import aiohttp
from traccar import API

URL = 'http://192.168.2.11:8082/api'


async def test():
    """Example usage of pytraccar."""
    async with aiohttp.ClientSession() as session:
        data = API(LOOP, session, 'admin', 'admin', URL)
        await data.get_device_info()

        print("Device info:", data.device_info)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(test())
