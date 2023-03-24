import json
import asyncio
import os
import re
from typing import List
from fastapi import FastAPI, Depends, Path, Query
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from web3 import Web3
from .cosmos import get_wallet_balances as cosmos_wallet_balances, get_cosmos_positions, write_tokens, return_farms_list as cosmos_farms_list, return_network_list as cosmos_network_list
from .evm import *
from .sol import get_wallet_balances as solana_wallet_balances, get_solana_positions, return_farms_list as solana_farms_list
from .terra import get_wallet_balances as terra_wallet_balances, get_terra_positions, return_farms_list as terra_farms_list
from .api.v1.api import router as api_router
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo
from .db.mongodb import AsyncIOMotorClient, get_database
from .db.database import SessionLocal
from .httpsession.session import ClientSession, get_session
from .httpsession.session_utils import session_start, session_stop
from .solsession.session import AsyncClient, get_solana
from .solsession.session_utils import solana_start, solana_stop
from .terrasession.session import AsyncLCDClient, get_terra
from .terrasession.session_utils import terra_start, terra_stop
from .db.queries import addresses_per_day, farms_over_last_30_days
from sqlalchemy.orm import Session
from sqlalchemy import tuple_, text
import ably.types.message as Message
import ably
import nats
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
from typing import Iterable, Any, Tuple

# from .db.postgres_utils import close_postgres_connection, connect_to_postgres
# from .db.postgres import Database, get_postgres_database
# from fastapi_profiler.profiler_middleware import PyInstrumentProfilerMiddleware
# from fastapi_profiler.profiler_middleware import PyInstrumentProfilerMiddleware

app = FastAPI(title='FastAPI')
# app.add_middleware(PyInstrumentProfilerMiddleware, profiler_output_type='html')

ably = ably.AblyRest(os.getenv("ABLY_KEY", ""))

MULTICALL_SPLIT_AMOUNT = int(os.getenv("MULTICALL_SPLIT_AMOUNT", 4))
ABLY_SEND = os.getenv("ABLY_SEND", "True") == "True"

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
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class DeletionItem(BaseModel):
    wallet: str
    signature: str
    timestamps: List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@app.get("/",  tags=["Endpoint Test"])
def main_endpoint_test():
    return {"message": "Test Message"}

@app.get('/native-balances/{wallet}')
async def native_balances(wallet):
    results = await return_native_balances(wallet)
    return results

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


@app.get('/supported_networks/')
async def get_supported_networks():

    networks = {
        'evm': return_network_list(),
        'cosmos': cosmos_network_list(),
        'solana': [],
        'terra': []
    }

    return networks


@app.get('/farms/{wallet}/{farm_id}')
async def get_farms(wallet, farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), pdb: Session = Depends(get_db)):
    results = await get_evm_positions(wallet, farm_id, mongo_db, session, None, pdb)
    return results

@app.get('/user-config/{wallet}/{farm_id}')
async def get_farms(wallet, farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), pdb: Session = Depends(get_db)):
    results = await get_evm_positions(wallet, farm_id, mongo_db, session, None, pdb, user_config=True)
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
    results = await get_cosmos_positions(wallet, farm_id, mongo_db, session, None, pdb)
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
    x = await db['full_tokens'].find_one({'tokenID': token_id, 'network': network}, {'_id': False})
    return x


@app.get('/user-balance/')
async def get_user_balances(wallet: List[str] = Query([]), farm_id: List[str] = Query([]), days: int = Query(..., ge=1, le=90), pdb: Session = Depends(get_db)):
    wallets = [f"'{wall}'" for wall in wallet if re.match(r"\w+$", wall)]

    if len(wallets) == 0:
        return []

    if farm_id:
        farms = [f"'{farm}'" for farm in farm_id if re.match(r"\w+$", farm)]
        if len(farms) == 0:
            return []

        x = await pdb.execute(text(f'''select bucket as _id, sum(dollarValue) as average from (
    SELECT
    bucket,
    farm_network, farm,
    avg(dollarValue) AS dollarValue
    FROM
    user_data_per_hour
    WHERE bucket > now () - INTERVAL '{days} days' and wallet IN ({','.join(wallets)}) and farm IN ({','.join(farms)})
    GROUP BY farm_network, farm, bucket
    ) a group by bucket ORDER BY _id ASC;'''))
    else:
        x = await pdb.execute(text(f'''select bucket as _id, sum(dollarValue) as average from (
    SELECT
    bucket,
    farm_network, farm,
    avg(dollarValue) AS dollarValue
    FROM
    user_data_per_hour
    WHERE bucket > now () - INTERVAL '{days} days' and wallet IN ({','.join(wallets)})
    GROUP BY farm_network, farm, bucket
    ) a group by bucket ORDER BY _id ASC;'''))

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
async def get_stats(type, pdb: Session = Depends(get_db)):

    if type == 'users':
        x = await pdb.execute(text(f'''SELECT
    time_bucket('1 days', timestamp) AS bucket,
    COUNT(DISTINCT(wallet))
    FROM
    user_data

    GROUP BY bucket ORDER BY bucket DESC'''))
    else:
        x = await pdb.execute(text(f'''
    SELECT
    time_bucket('1 days', timestamp) AS bucket,
    farm,
    COUNT(DISTINCT(wallet))
    FROM
    user_data

    GROUP BY bucket,farm ORDER BY bucket DESC, count DESC'''))

    return x.fetchall()


@app.get('/healthcheck')
async def health_check(db: AsyncIOMotorClient = Depends(get_database)):
    return {"status": "ok"}

multicall_methods_translator = {
    'solana-farms': get_solana_positions,
    'cosmos-farms': get_cosmos_positions,
    'terra-farms': get_terra_positions,
    'farms': get_evm_positions,
    'wallet': lambda *args: get_wallet_balance(args[0], args[1], args[2], args[3], args[4]),
    'cosmos-wallet': lambda *args: cosmos_wallet_balances(args[0], args[2], args[3], args[5]),
    'terra-wallet': lambda *args: terra_wallet_balances(args[0], args[2], args[3], args[5]),
    'solana-wallet': lambda *args: solana_wallet_balances(args[0], args[2], args[3], args[5]),
}


async def execute_call(*args, method_name=None, mongo_db=None, session=None, client=None, pdb=None, req_id=None):
    # channel = ably.channels.get(req_id)

    try:
        method = multicall_methods_translator[method_name]
        results = await method(*args, mongo_db, session, client, pdb)
        if results:
            # print(f"results for {method_name} {results}")
            # channel.publish_message(Message.Message(name=req_id, data=results))
            return results
        else:
            # print(f"No results for {method_name} {args}")
            return {"wallet": args[0], "params": args[1:]}

    except Exception as e:
        print(f'{e} wallet: {args[0]}, params: {args[1:]}')
        return {"wallet": args[0], "params": args[1:], "error": f"{type(e)}: {e}"}


async def execute_multi_call(wallet, all_params, method_name=None, mongo_db=None, session=None, client=None, pdb=None, req_id=None):
    if ABLY_SEND:
        channel = ably.channels.get(req_id)

    results = await asyncio.gather(*[execute_call(wallet, params, method_name=method_name, mongo_db=mongo_db,
                                                  session=session, client=client, pdb=pdb, req_id=req_id) for params in all_params])
    if not ABLY_SEND:
        for result in results:
            print(result)

        print("\n\n")

    if ABLY_SEND:
        channel.publish_message(Message.Message(name=req_id, data=results))


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


@app.post('/multicall')
async def multicall(request: Request, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), pdb: Session = Depends(get_db), client_terra: AsyncLCDClient = Depends(get_terra), client_solana: AsyncClient = Depends(get_solana)):
    farms_clients = {'solana-farms': client_solana, 'cosmos-farms': None, 'terra-farms': client_terra, 'farms': None,
                     'solana-wallet': client_solana, 'cosmos-wallet': None, 'terra-wallet': client_terra, 'wallet': None}

    body_json = await request.json()

    loop = asyncio.get_event_loop()

    req_id = request.headers.get('X-CHANNEL-ID')
    for method in body_json.keys():
        for wallet in body_json[method].keys():
            params = body_json[method][wallet]

            if not params:
                params = ['']

            for chunked_params in list(chunks(params, MULTICALL_SPLIT_AMOUNT)):
                loop.create_task(execute_multi_call(wallet, chunked_params, method_name=method, mongo_db=mongo_db,
                                                    session=session, client=farms_clients[method], pdb=pdb, req_id=req_id))

                await asyncio.sleep(0.05)

    return {"status": "ok", "channel": req_id}



natspool = {}


async def execute_call2(*args, method_name=None, mongo_db=None, session=None, client=None, pdb=None, req_id=None):
    # channel = ably.channels.get(req_id)

    try:
        method = multicall_methods_translator[method_name]
        results = await method(*args, mongo_db, session, client, pdb)
        if results:
            # print(f"results for {method_name} {results}")
            # channel.publish_message(Message.Message(name=req_id, data=results))
            return results
        else:
            pass
            # print(f"No results for {method_name} {args}")
            # return {"wallet": args[0], "params": args[1:]}

    except Exception as e:
        print(e)

        return {"wallet": args[0], "params": args[1:], "error": f"{type(e)}: {e}"}


async def execute_multi_call2(wallet, all_params, method_name=None, mongo_db=None, session=None, client=None, pdb=None, req_id=None, last = False):
    results = await asyncio.gather(*[execute_call2(wallet, params, method_name=method_name, mongo_db=mongo_db,
                                                  session=session, client=client, pdb=pdb, req_id=req_id) for params in all_params])
    if not ABLY_SEND:
        for result in results:
            print(result)

        print("\n\n")

    data=list(filter(None, results))

    nats_server = natspool['nats']

    if nats_server and len(data) > 0:
        await nats_server.publish(req_id, bytes(json.dumps(data[0]), 'ascii'))


@app.post('/multicall2')
async def multicall2(request: Request, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), pdb: Session = Depends(get_db), client_terra: AsyncLCDClient = Depends(get_terra), client_solana: AsyncClient = Depends(get_solana)):
    # server = await nats.connect("nats://54.36.175.103:4222")
    if 'nats' not in natspool.keys():
        natspool['nats'] = await nats.connect("nats://54.36.175.103:4222")
   
    farms_clients = {'solana-farms': client_solana, 'cosmos-farms': None, 'terra-farms': client_terra, 'farms': None,
                     'solana-wallet': client_solana, 'cosmos-wallet': None, 'terra-wallet': client_terra, 'wallet': None}

    body_json = await request.json()

    loop = asyncio.get_event_loop()

    req_id = request.headers.get('X-CHANNEL-ID')
    for method in body_json.keys():
        for wallet in body_json[method].keys():
            params = body_json[method][wallet]

            if not params:
                params = ['']

            for chunked_params in list(chunks(params, 1)):
                loop.create_task(execute_multi_call2(wallet, chunked_params, method_name=method, mongo_db=mongo_db,
                                                    session=session, client=farms_clients[method], pdb=pdb, req_id=req_id))

    return {"status": "ok", "channel": req_id}

@app.post('/user-active-pools')
async def user_active_pools(request: Request, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session), pdb: Session = Depends(get_db), client_terra: AsyncLCDClient = Depends(get_terra), client_solana: AsyncClient = Depends(get_solana)):
    body_json = await request.json()
    wallet = body_json['address']
    walletType = body_json['type']


    farms_clients = {'solana-farms': client_solana, 'cosmos-farms': None, 'terra-farms': client_terra, 'farms': None,
                    'solana-wallet': client_solana, 'cosmos-wallet': None, 'terra-wallet': client_terra, 'wallet': None}
    
    if 'nats' not in natspool.keys():
        natspool['nats'] = await nats.connect("nats://54.36.175.103:4222")

    loop = asyncio.get_event_loop()

    req_id = request.headers.get('X-CHANNEL-ID')

    if walletType == 'evm':
        # get chains
        methodName = 'farms'
        results = await return_native_balances(wallet)
        chains = []
        for k,v in results.items():
            if v > 0:
                chains.append(k) #

        farm_list = return_farms_list()
        farms = [farm_list[x]['masterChef'] for x in farm_list if 'show' not in farm_list[x] and farm_list[x]['network'] in chains ]
    elif walletType == 'cosmos':
        methodName = 'cosmos-farms'
        farm_list = cosmos_farms_list()
        farms = [farm_list[x]['masterChef'] for x in farm_list if 'show' not in farm_list[x]]
    elif walletType == 'terra':
        methodName = 'terra-farms'
        farm_list = terra_farms_list()
        farms = [farm_list[x]['masterChef'] for x in farm_list if 'show' not in farm_list[x]]
    elif walletType == 'solana':
        methodName = 'solana-farms'
        farm_list = solana_farms_list()
        farms = [farm_list[x]['masterChef'] for x in farm_list if 'show' not in farm_list[x]]
    else:
        farms = []
        print(f"Unknown wallet type <<<<<<<<<<<<<<<<<<<<<< {walletType}")

    try: 
        for farm in farms:
            try:
                loop.create_task(execute_multi_call2(wallet, [farm], method_name=methodName, mongo_db=mongo_db, session=session,
                                                     client=farms_clients[methodName], pdb=pdb, req_id=req_id, last=False))
            except Exception as e:
                print(f"Error in farm {farm} {wallet} {methodName} {e}")


        return {"status": "ok", "channel": req_id, 'farmsCount': len(farms)}
    except Exception as e:
        print(f"Error in user_active_pools {e} {farms}")
        return {"status": "ko", "channel": req_id, 'error': str(e)}

@app.get('/historical-transactions-osmosis/{wallet}/{poolid}')
async def historical_transactions_osmosis(wallet, poolid, ClientSession = Depends(get_session), pdb: Session = Depends(get_db)):
    join_pool = await pdb.execute(text(f'''select
block_height,
block_timestamp,
tx_id,
pool_id,
token_in,
amount_in
FROM public.join_pool_unnest
where sender = '{wallet}' and pool_id = '{poolid}';'''))

    exit_pool = await pdb.execute(text(f'''select
block_height,
block_timestamp,
tx_id,
pool_id,
token_out,
amount_out
FROM public.exit_pool_unnest
where sender = '{wallet}' and pool_id = '{poolid}';'''))

    return {'joins' : join_pool.fetchall(), 'exits' : exit_pool.fetchall()} 

