from terra_sdk.client.lcd import AsyncLCDClient

class TerraClient:
    session: AsyncLCDClient = None

terra_client= TerraClient()

async def get_terra() -> AsyncLCDClient:
    return terra_client.session
