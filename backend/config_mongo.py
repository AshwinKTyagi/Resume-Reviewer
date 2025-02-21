import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/authDB")
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")

# Create a MongoDB client
client = MongoClient(MONGO_URI)

# Get the database and collection
db = client.get_database("resume_reviewer")
users_collection = db.get_collection("auth_collection")
resume_collection = db.get_collection("resume_collection")

