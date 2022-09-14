from .session import terra_client
from terra_sdk.client.lcd import AsyncLCDClient

async def terra_start():
    #terra_client.session = AsyncLCDClient("https://dark-damp-butterfly.terra-mainnet.quiknode.pro/770d97d8b71b8708126373ab8d5ca981c1f48e71/", "columbus-5")
    terra_client.session = AsyncLCDClient("https://lcd.terra.dev/", "columbus-5")

async def terra_stop(self):
    await terra_client.session.close()
    terra_client.session = None