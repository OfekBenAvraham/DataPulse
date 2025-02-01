# connection.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "datapulse_tracker")

client = AsyncIOMotorClient(DATABASE_URL)
database = client[DATABASE_NAME]

# Collections
peer_collection = database["peers"]
file_collection = database["files"]
