from fastapi import FastAPI, Depends, Path
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from toolz.itertoolz import get
from evm import return_farms_list, get_evm_positions, get_wallet_balance, scan_ethlogs_approval, get_tx_to_contract
from cosmos import get_wallet_balances as cosmos_wallet_balances, get_cosmos_positions, write_tokens, return_farms_list as cosmos_farms_list
from sol import get_wallet_balances as solana_wallet_balances, get_solana_positions, return_farms_list as solana_farms_list
from api.v1.api import router as api_router
from db.mongodb_utils import close_mongo_connection, connect_to_mongo
from db.mongodb import AsyncIOMotorClient, get_database
from httpsession.session import ClientSession, get_session
from httpsession.session_utils import session_start, session_stop
from solsession.session import AsyncClient, get_solana
from solsession.session_utils import solana_start, solana_stop
from fastapi_profiler.profiler_middleware import PyInstrumentProfilerMiddleware

app = FastAPI(title='FastAPI')
#app.add_middleware(PyInstrumentProfilerMiddleware, profiler_output_type='html')

# app.add_event_handler("startup", connect_to_mongo)
# app.add_event_handler("shutdown", close_mongo_connection)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    await session_start()
    await solana_start()

@app.on_event("shutdown")
def shutdown_event():
    close_mongo_connection()
    session_stop()
    solana_stop()


app.include_router(api_router, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["x-apigateway-header", "Content-Type", "X-Amz-Date"],
)

@app.get("/",  tags=["Endpoint Test"])
def main_endpoint_test():
    return {"message": "Test Message"}

@app.get('/solana-wallet/{wallet}')
async def read_results(wallet, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), client: AsyncClient = Depends(get_solana)):
    results = await solana_wallet_balances(wallet, mongo_db, session, client)
    return results

@app.get('/farms-list/')
async def get_farm_list():
    farm_list = {**return_farms_list(), **cosmos_farms_list(), **solana_farms_list()}
    results = [{'sendValue' : farm_list[x]['masterChef'], 'name' : farm_list[x]['name'], 'network': farm_list[x]['network'], 'featured' : farm_list[x]['featured']} for x in farm_list if 'show' not in farm_list[x]]
    return results

@app.get('/farms/{wallet}/{farm_id}')
async def get_farms(wallet,farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await get_evm_positions(wallet, farm_id, mongo_db, session)
    return results

@app.get('/cosmos-farms/{wallet}/{farm_id}')
async def get_cosmos_farms(wallet,farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await get_cosmos_positions(wallet, farm_id, mongo_db, session)
    return results

@app.get('/solana-farms/{wallet}/{farm_id}')
async def get_solana_farms(wallet,farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), client: AsyncClient = Depends(get_solana)):
    results = await get_solana_positions(wallet, farm_id, mongo_db, session, client)
    return results

@app.get('/wallet/{wallet}/{network}')
async def wallet_balance(wallet,network, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await get_wallet_balance(wallet, network, mongo_db, session)
    return results

@app.get('/cosmos-wallet/{wallet}')
async def cosmos_wallet_balance(wallet, session: ClientSession = Depends(get_session), mongo_db: AsyncIOMotorClient = Depends(get_database)):
    results = await cosmos_wallet_balances(wallet,session, mongo_db)
    return results

@app.get('/tokens/{network}/{token_id}')
async def get_tokens(db: AsyncIOMotorClient = Depends(get_database), token_id:str = Path(..., min_length=1), network:str = Path(..., min_length=1)):
    x = await db.xtracker['full_tokens'].find_one({'tokenID' : token_id, 'network' : network}, {'_id': False})
    return x

@app.get('/token-approval/{wallet}/{network}')
async def get_token_approvals(wallet,network, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await scan_ethlogs_approval(network, wallet, session, mongo_db)
    return results

@app.get('/historical-transactions/{network}/{wallet}/{contract}/{token}')
async def historical_transactions(wallet,network,contract,token, session: ClientSession = Depends(get_session)):
    results = await get_tx_to_contract(network, wallet, token, contract, session)
    return results

# @app.get('/write-tokens/{wallet}')
# async def get_cosmos_farms(wallet, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
#     results = await write_tokens(wallet, mongo_db, session)
#     return results
 
# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)

