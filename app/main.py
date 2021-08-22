from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from sol import funcs as sol
from api.v1.api import router as api_router

app = FastAPI(title='Serverless Lambda FastAPI')

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
    results = await sol.local_balances(wallet)
    return results

# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)

