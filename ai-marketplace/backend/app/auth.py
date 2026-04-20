from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

fake_db = {}

def hash_password(password):
    return pwd_context.hash(password[:72])

def verify_password(password, hashed):
    return pwd_context.verify(password[:72], hashed)

def create_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])