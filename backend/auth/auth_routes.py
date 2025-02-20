from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from config import users_collection
import auth_utils

auth_router = APIRouter()

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str
    
@auth_router.post("/register")
async def register(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth_utils.hash_password(user.password)
    users_collection.insert_one({"username": user.username, "email": user.email, "password": hashed_password})
    
    return {"message": "User registered successfully"}

@auth_router.post("/login")
async def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not auth_utils.verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = auth_utils.create_jwt_token(str(db_user["_id"]))
    return {"access_token": token, "user": {"username": db_user["username"], "email": db_user["email"]}}