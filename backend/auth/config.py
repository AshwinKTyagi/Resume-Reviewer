import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/authDB")
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")

client = MongoClient(MONGO_URI)
db = client.get_database("authDB")
users_collection = db.get_collection("users")

