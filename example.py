"""Example usage of pytraccar."""
import asyncio

import aiohttp

from pytraccar import ApiClient


async def test():
    """Example usage of pytraccar."""
    async with aiohttp.ClientSession() as client_session:
        client = ApiClient(
            host="127.0.0.1",
            username="admin",
            password="Password123!",
            client_session=client_session,
        )
        print(await client.get_server())


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(test())
