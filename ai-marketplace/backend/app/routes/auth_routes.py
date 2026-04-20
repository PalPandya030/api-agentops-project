from fastapi import APIRouter
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import *

router = APIRouter()

@router.post("/signup")
def signup(username: str, password: str):
    fake_db[username] = hash_password(password)
    return {"msg": "User created"}

@router.post("/login")
def login(username: str, password: str):
    if username not in fake_db:
        return {"error": "User not found"}

    if not verify_password(password, fake_db[username]):
        return {"error": "Wrong password"}

    token = create_token({"user": username})
    return {"token": token}