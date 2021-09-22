from .session import solana_client
from solana.rpc.async_api import AsyncClient

async def solana_start():
    solana_client.session = AsyncClient('https://api.mainnet-beta.solana.com')

async def solana_stop(self):
    await solana_client.session.close()
    solana_client.session = None