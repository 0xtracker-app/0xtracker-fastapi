from .session import terra_client
from terra_sdk.client.lcd import AsyncLCDClient

async def terra_start():
    terra_client.session = AsyncLCDClient("https://lcd.terra.dev", "columbus-5")

async def terra_stop(self):
    await terra_client.session.close()
    terra_client.session = None