"""Example usage of pytraccar."""

import asyncio
import logging
import os

import aiohttp

from pytraccar import ApiClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)


async def test() -> None:
    """Example usage of pytraccar."""
    async with aiohttp.ClientSession(
        cookie_jar=aiohttp.CookieJar(unsafe=True)
    ) as client_session:
        client = ApiClient(
            host=os.environ["TRACCAR_HOST"],
            port=os.environ.get("TRACCAR_PORT", 8082),
            username=os.environ["TRACCAR_USERNAME"],
            password=os.environ["TRACCAR_PASSWORD"],
            client_session=client_session,
        )
        server = await client.get_server()
        logging.info(
            "Connected to Traccar server (%s:%s) which is running version %s",
            os.environ["TRACCAR_HOST"],
            os.environ.get("TRACCAR_PORT", 8082),
            server["version"],
        )


asyncio.run(test())
