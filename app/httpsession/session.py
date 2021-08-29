from aiohttp import ClientSession

class HttpClient:
    session: ClientSession = None


http_client = HttpClient()


async def get_session() -> ClientSession:
    return http_client.session
