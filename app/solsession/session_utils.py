from .session import solana_client
from solana.rpc.async_api import AsyncClient

async def solana_start():
    #solana_client.session = AsyncClient('https://api.mainnet-beta.solana.com')
    solana_client.session = AsyncClient('https://red-frosty-darkness.solana-mainnet.quiknode.pro/a0c12c0d9b2fc3400fe2fd228e5271b2b7a7d497/')

async def solana_stop(self):
    await solana_client.session.close()
    solana_client.session = None