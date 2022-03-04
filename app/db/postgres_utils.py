from databases import Database
from .postgres import postdb
import os
from dotenv import load_dotenv

async def connect_to_postgres():
    postdb.client = await Database(os.getenv("POSTGRES_URL"),
                              min_size=5,
                              max_size=20).connect()

async def close_postgres_connection():
    postdb.client.close()