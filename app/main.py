from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from toolz.itertoolz import get
from sol import funcs as sol_funcs
from evm import return_farms_list, get_evm_positions
from api.v1.api import router as api_router

app = FastAPI(title='0xTracker FastAPI')

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
async def get_farms(wallet,farm_id):
    results = await get_evm_positions(wallet, farm_id)
    return results

# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)

