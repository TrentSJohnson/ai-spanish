import os

from motor.motor_asyncio import AsyncIOMotorClient


class BaseDBService:
    def __init__(self):
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "aispanish")
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client[database_name]
