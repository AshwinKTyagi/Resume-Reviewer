from passlib.context import CryptContext
import jwt
import datetime
from config import JWT_SECRET

# Initialize the password context with bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a password against its hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create a JWT token for a user
def create_jwt_token(user_id: str) -> str:
    to_encode = {
        "sub": user_id,
        "exp": datetime.datetime.now(tz="utc") + datetime.timedelta(days=1)
    }
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return encoded_jwt

# Function to verify a JWT token
def verify_jwt(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
