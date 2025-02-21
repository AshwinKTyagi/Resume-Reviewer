from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .config_mongo import users_collection
from . import auth_utils

auth_router = APIRouter()

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str
    
@auth_router.get("/")
async def root():
    return {"message": "Welcome to the authentication service"}

@auth_router.post("/register/")
async def register(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth_utils.hash_password(user.password)
    
    new_user = {
        "username": user.username,
        "email": user.email, 
        "password": hashed_password
    }
    
    users_collection.insert_one(new_user)
    
    return {"message": "User registered successfully"}

@auth_router.post("/login/")
async def login(user: UserLogin):
    print(user)
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not auth_utils.verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = auth_utils.create_jwt_token(str(db_user["_id"]))
    
    user =  {"access_token": token, "user": {"username": db_user["username"], "email": db_user["email"]}}
    print(user)
    return user

@auth_router.get("/protected/")
async def protected_route(token: str = Depends(auth_utils.verify_jwt)):
    if not token:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    return {"message": "You have access!", "user_id": token}

