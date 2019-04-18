"""Cli tools,"""
import asyncio
import aiohttp
from api import API


async def test():
    """Debug of pytraccar."""
    async with aiohttp.ClientSession() as session:
        host = input("IP: ")
        username = input("Username: ")
        password = input("Password: ")
        print("\n\n\n")
        data = API(LOOP, session, username, password, host)
        await data.test_connection()
        print("Authenticated:", data.authenticated)
        if data.authenticated:
            await data.get_device_info()
            print("Authentication:", data.authenticated)
            print("Geofences:", data.geofences)
            print("Devices:", data.devices)
            print("Positions:", data.positions)
            print("Device info:", data.device_info)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(test())
