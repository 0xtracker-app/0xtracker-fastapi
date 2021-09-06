from fastapi import FastAPI, Depends, Path
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from toolz.itertoolz import get
from sol import funcs as sol_funcs
from evm import return_farms_list, get_evm_positions
from api.v1.api import router as api_router
from db.mongodb_utils import close_mongo_connection, connect_to_mongo
from db.mongodb import AsyncIOMotorClient, get_database
from httpsession.session import ClientSession, get_session
from httpsession.session_utils import session_start, session_stop
from fastapi_profiler.profiler_middleware import PyInstrumentProfilerMiddleware

app = FastAPI(title='FastAPI')
#app.add_middleware(PyInstrumentProfilerMiddleware, profiler_output_type='html')

# app.add_event_handler("startup", connect_to_mongo)
# app.add_event_handler("shutdown", close_mongo_connection)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    await session_start()

@app.on_event("shutdown")
def shutdown_event():
    close_mongo_connection()
    session_stop()


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
async def read_results(wallet):
    results = await sol_funcs.local_balances(wallet)
    return results

@app.get('/farms-list/')
async def get_farm_list():
    farm_list = return_farms_list()
    results = [{'sendValue' : farm_list[x]['masterChef'], 'name' : farm_list[x]['name'], 'network': farm_list[x]['network'], 'featured' : farm_list[x]['featured']} for x in farm_list if 'show' not in farm_list[x]]
    return results

@app.get('/farms/{wallet}/{farm_id}')
async def get_farms(wallet,farm_id, mongo_db: AsyncIOMotorClient = Depends(get_database), session: ClientSession = Depends(get_session)):
    results = await get_evm_positions(wallet, farm_id, mongo_db, session)
    return results

@app.get('/tokens/{network}/{token_id}')
async def get_tokens(db: AsyncIOMotorClient = Depends(get_database), token_id:str = Path(..., min_length=1), network:str = Path(..., min_length=1)):
    x = await db.xtracker['full_tokens'].find_one({'tokenID' : token_id, 'network' : network}, {'_id': False})
    return x

# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)

