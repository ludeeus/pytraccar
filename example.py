"""Example usage of pytraccar."""
import asyncio
import aiohttp
from pytraccar.api import API

HOST = "192.168.2.105"
PORT = 8072


async def test():
    """Example usage of pytraccar."""
    async with aiohttp.ClientSession() as session:
        data = API(LOOP, session, "admin", "admin", HOST, PORT)
        await data.get_device_info()

        print()
        print("device_info:", data.device_info)
        print()
        print("positions:", data.positions)
        print()
        print("devices:", data.devices)
        print()
        print("geofences:", data.geofences)
        print()
        print("events:", data.events)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(test())
