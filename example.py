"""Example usage of pytraccar."""
import asyncio
import aiohttp
from pytraccar.api import API

HOST = "192.168.2.11"


async def test():
    """Example usage of pytraccar."""
    async with aiohttp.ClientSession() as session:
        data = API(LOOP, session, "admin", "admin", HOST)
        await data.get_device_info()

        print("Device info:", data.device_info)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(test())
