import logging
import os

from dotenv import load_dotenv
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBConnection:
    
    def __init__(self):
        """ Initialize MongoDB connection and database """
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGODB_DATABASE", "chatbot_db")
        
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            
            # Test the connection
            self.client.admin.command('ping')
            print("MongoDB connection successful.")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")
        
    def get_collection(self, collection_name: str):
        """ Get a specific collection from the database """
        try: 
            return self.db[collection_name]
        except Exception as e:
            logger.error(f"Failed to get collection {collection_name}: {str(e)}")
            raise RuntimeError(f"Failed to get collection {collection_name}: {str(e)}")

    def close(self):
        """ Close the MongoDB connection """
        try:
            self.client.close()
            print("MongoDB connection closed.")
        except Exception as e:
            logger.error(f"Failed to close MongoDB connection: {str(e)}")
            raise RuntimeError(f"Failed to close MongoDB connection: {str(e)}")
    