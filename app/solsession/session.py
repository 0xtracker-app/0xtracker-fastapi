from solana.rpc.async_api import AsyncClient

class SolanaClient:
    session: AsyncClient = None

solana_client = SolanaClient()

async def get_solana() -> AsyncClient:
    return solana_client.session
