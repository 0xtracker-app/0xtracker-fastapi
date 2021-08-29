from .session import http_client
from aiohttp import ClientSession

async def session_start():
    http_client.session = ClientSession()

async def session_stop(self):
    await http_client.session.close()
    http_client.session = None