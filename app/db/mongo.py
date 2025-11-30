from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings
from app.core.constants import MONGO_DB_NAME

class MongoDBClient:
    client: AsyncIOMotorClient = None
    db = None

    def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            self.db = self.client[MONGO_DB_NAME]
            print("succesfully connected to mongo")
        except Exception as e:
            print(f"mongo connection error: {e}")

    def close(self):
        if self.client:
            self.client.close()
            print("mongo connection is closed")


mongo_client = MongoDBClient()

def get_db():
    return mongo_client.db