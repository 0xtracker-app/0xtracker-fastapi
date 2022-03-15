from motor.motor_asyncio import AsyncIOMotorClient
import os

DATABASE_NAME = os.getenv("MONGO_DB")

class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client[DATABASE_NAME]