"""Example usage of pytraccar."""
import asyncio
import aiohttp
from pytraccar.api import API

HOST = "192.168.100.3"
PORT = 8072
USERNAME = "admin"
PASSWORD = "admin"


async def test():
    """Example usage of pytraccar."""
    async with aiohttp.ClientSession() as session:
        data = API(LOOP, session, USERNAME, PASSWORD, HOST, PORT)
        await data.get_device_info()
        await data.get_events([2])

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
