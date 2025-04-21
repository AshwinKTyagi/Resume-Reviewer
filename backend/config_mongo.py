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

# Ensure the database and collections are created and initialized
if "resume_reviewer" not in client.list_database_names():
    # Initialize the database with required collections
    db.create_collection("auth_collection")
    db.create_collection("resume_collection")
    print("Database and collections created successfully.")
else:
    print("Database already exists.")
