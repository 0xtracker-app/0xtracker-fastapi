from time import sleep
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id 
from typing import List, Optional, Tuple
from fastapi import FastAPI, Depends, Path, Query, BackgroundTasks
from pydantic import BaseModel
from typing import List
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from toolz.itertoolz import get
from .cosmos import get_wallet_balances as cosmos_wallet_balances, get_cosmos_positions, write_tokens, return_farms_list as cosmos_farms_list
from .evm import *
from .sol import get_wallet_balances as solana_wallet_balances, get_solana_positions, return_farms_list as solana_farms_list
from .terra import get_wallet_balances as terra_wallet_balances, get_terra_positions, return_farms_list as terra_farms_list
from .api.v1.api import router as api_router
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo
from .db.mongodb import AsyncIOMotorClient, get_database
from .db.postgres_utils import close_postgres_connection, connect_to_postgres
from .db.postgres import Database, get_postgres_database
from .db.database import SessionLocal, engine
from .db import crud, models, schemas
from .httpsession.session import ClientSession, get_session
from .httpsession.session_utils import session_start, session_stop
from .solsession.session import AsyncClient, get_solana
from .solsession.session_utils import solana_start, solana_stop
from .terrasession.session import AsyncLCDClient, get_terra
from .terrasession.session_utils import terra_start, terra_stop
from fastapi_profiler.profiler_middleware import PyInstrumentProfilerMiddleware
from .db.queries import user_info_by_time, addresses_per_day, farms_over_last_30_days
from sqlalchemy.orm import Session
from starlette.requests import Request

app = FastAPI(title='FastAPI')
app.add_middleware(CorrelationIdMiddleware)
#app.add_middleware(PyInstrumentProfilerMiddleware, profiler_output_type='html')

# app.add_event_handler("startup", connect_to_mongo)
# app.add_event_handler("shutdown", close_mongo_connection)


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    # await connect_to_postgres()
    await session_start()
    await solana_start()
    await terra_start()


@app.on_event("shutdown")
def shutdown_event():
    close_mongo_connection()
    # close_postgres_connection()
    session_stop()
    solana_stop()
    terra_stop()


app.include_router(api_router, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["x-apigateway-header", "Content-Type", "X-Amz-Date"],
)


class DeletionItem(BaseModel):
    wallet: str
    signature: str
    timestamps: List


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/",  tags=["Endpoint Test"])
def main_endpoint_test():
    return {"message": "Test Message"}


@app.get('/solana-wallet/{wallet}')
async def read_results(wallet, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), client: AsyncClient = Depends(get_solana), pdb: Session = Depends(get_db)):
    results = await solana_wallet_balances(wallet, mongo_db, session, client, pdb)
    return results


@app.get('/terra-wallet/{wallet}')
async def read_results(wallet, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), client: AsyncLCDClient = Depends(get_terra), pdb: Session = Depends(get_db)):
    results = await terra_wallet_balances(wallet, mongo_db, session, client, pdb)
    return results


@app.get('/farms-list/')
async def get_farm_list():
    farm_list = {**return_farms_list(), **cosmos_farms_list(), **
                 solana_farms_list(), **terra_farms_list()}
    results = [{'sendValue': farm_list[x]['masterChef'], 'name': farm_list[x]['name'], 'network': farm_list[x]
                ['network'], 'featured': farm_list[x]['featured']} for x in farm_list if 'show' not in farm_list[x]]
    return results


@app.get('/farms/{wallet}/{farm_id}')
async def get_farms(wallet, farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), pdb: Session = Depends(get_db)):
    results = await get_evm_positions(wallet, farm_id, mongo_db, session, pdb)
    return results


@app.get('/apy/{farm_id}')
async def get_apy(farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await get_protocol_apy(farm_id, mongo_db, session)
    return results


@app.get('/apy-list/')
async def get_apy_list(filter: str = None):
    results = return_apy_list(filter)
    return results

# @app.get('/all_apy/', include_in_schema=True)
# async def get_apy(mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
#     results = await get_all_protocols(mongo_db, session)
#     return results


@app.get('/apy_dex/')
async def apy_dex(mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await get_dex_info(mongo_db, session)
    return results


@app.get('/voltswap_tvl/{network}')
async def voltswap_tvl(network, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await get_voltswap_llama(mongo_db, session, network)
    return results


@app.get('/passport_tvl')
async def passport_tvl(mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await get_passport_llama(mongo_db, session)
    return results


@app.post("/delete_user_records/")
async def create_item(item: DeletionItem, mongo_db: AsyncIOMotorClient = Depends(get_database), pdb: Session = Depends(get_db)):
    result = await delete_user_records(item.wallet, item.signature, item.timestamps, mongo_db, pdb)
    return result


@app.get('/cosmos-farms/{wallet}/{farm_id}')
async def get_cosmos_farms(wallet, farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), pdb: Session = Depends(get_db)):
    results = await get_cosmos_positions(wallet, farm_id, mongo_db, session, pdb)
    return results


@app.get('/solana-farms/{wallet}/{farm_id}')
async def get_solana_farms(wallet, farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), client: AsyncClient = Depends(get_solana), pdb: Session = Depends(get_db)):
    results = await get_solana_positions(wallet, farm_id, mongo_db, session, client, pdb)
    return results


@app.get('/terra-farms/{wallet}/{farm_id}')
async def get_terra_farms(wallet, farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), client: AsyncLCDClient = Depends(get_terra), pdb: Session = Depends(get_db)):
    results = await get_terra_positions(wallet, farm_id, mongo_db, session, client, pdb)
    return results


@app.get('/wallet/{wallet}/{network}')
async def wallet_balance(wallet, network, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), pdb: Session = Depends(get_db)):
    results = await get_wallet_balance(wallet, network, mongo_db, session, pdb)
    return results


@app.get('/cosmos-wallet/{wallet}')
async def cosmos_wallet_balance(wallet, session: ClientSession = Depends(get_session), mongo_db: AsyncIOMotorClient = Depends(get_database), pdb: Session = Depends(get_db)):
    results = await cosmos_wallet_balances(wallet, session, mongo_db, pdb)
    return results


@app.get('/tokens/{network}/{token_id}')
async def get_tokens(db: AsyncIOMotorClient = Depends(get_database), token_id: str = Path(..., min_length=1), network: str = Path(..., min_length=1)):
    x = await db.xtracker['full_tokens'].find_one({'tokenID': token_id, 'network': network}, {'_id': False})
    return x


@app.get('/user-balance/')
async def get_user_balances(wallet: List[str] = Query([]), farm_id: List[str] = Query([]), days: int = Query(..., ge=1, le=90), pdb: Session = Depends(get_db)):

    if farm_id:
        x = pdb.execute(f'''select bucket as _id, sum(dollarValue) as average from (
    SELECT
    time_bucket('1 hour', timestamp) AS bucket,
    farm_network, farm,
    avg(dollarValue) AS dollarValue
    FROM
    user_data
    WHERE timestamp > now () - INTERVAL ':days days' and wallet IN :wallets and farm IN :farms
    GROUP BY farm_network, farm, bucket
    ) a group by bucket;''', {"days": days, "wallets": tuple(wallet), "farms": tuple(farm_id)})
    else:
        x = pdb.execute(f'''select bucket as _id, sum(dollarValue) as average from (
    SELECT
    time_bucket('1 hour', timestamp) AS bucket,
    farm_network, farm,
    avg(dollarValue) AS dollarValue
    FROM
    user_data
    WHERE timestamp > now () - INTERVAL ':days days' and wallet IN :wallets
    GROUP BY farm_network, farm, bucket
    ) a group by bucket;''', {"days": days, "wallets": tuple(wallet)})

    return x.fetchall()


@app.get('/token-approval/{wallet}/{network}')
async def get_token_approvals(wallet, network, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await scan_ethlogs_approval(network, wallet, session, mongo_db)
    return results


@app.get('/historical-transactions/{network}/{wallet}/{contract}/{token}')
async def historical_transactions(wallet, network, contract, token, session: ClientSession = Depends(get_session)):
    results = await get_tx_to_contract(network, wallet, token, contract, session)
    return results


@app.get('/stats/{type}', include_in_schema=False)
async def get_stats(type, db: AsyncIOMotorClient = Depends(get_database)):

    stat_types = {
        "users": db.xtracker['user_data'].aggregate(addresses_per_day()),
        "farms": db.xtracker['user_data'].aggregate(farms_over_last_30_days())
    }

    x = await stat_types[type].to_list(length=None)

    return x


@app.get('/healthcheck')
async def health_check(db: AsyncIOMotorClient = Depends(get_database)):
    return {"status": "ok"}


get_farms_methods = { 'solana-farms': get_solana_positions,
    'cosmos-farms': get_cosmos_positions,
    'terra-farms': get_terra_positions,
    'farms': get_evm_positions }

async def background_get_farms(req_id, method, wallet, farm, mongo_db, session, pdb):
    print(f'{req_id} {method} {wallet} {farm}')
    # get_farms_methods[method](wallet, farm, mongo_db, session, pdb)


@app.post('/multicall')
async def multicall(request: Request, background_tasks: BackgroundTasks, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), pdb: Session = Depends(get_db)):
    body_json = await request.json()
    req_id = correlation_id.get()
    for method in body_json.keys():
        for wallet in body_json[method].keys():
            for farm in body_json[method][wallet]:
                background_tasks.add_task(background_get_farms, req_id, method, wallet, farm, mongo_db, session, pdb)

    return {"status": "ok", "channel": req_id}


# @app.get("/users/")
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users

# @app.get('/router-details/{network}/{contract}')
# async def router_details(network, contract, session: ClientSession = Depends(get_session)):
#     results = await get_router_details(network, contract, session)
#     return results

# @app.get('/write-tokens/{wallet}')
# async def get_cosmos_farms(wallet, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
#     results = await write_tokens(wallet, mongo_db, session)
#     return results

# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)
