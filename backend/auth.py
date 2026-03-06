import os
import hashlib
import secrets
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# MongoDB Connection
MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.safetrack
users_collection = db.users


class User(BaseModel):
    full_name: str
    email: str
    password: str
    role: Optional[str] = "patient"  # patient or doctor


class UserLogin(BaseModel):
    email: str
    password: str


# --- Auth Helpers using built-in hashlib (no extra deps needed) ---
def get_password_hash(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt, stored_hash = hashed_password.split(":")
        computed = hashlib.sha256((salt + plain_password).encode()).hexdigest()
        return computed == stored_hash
    except Exception:
        return False


@router.post("/register")
async def register(user: User):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    user_dict["created_at"] = datetime.now().isoformat()

    new_user = await users_collection.insert_one(user_dict)
    return {"status": "success", "user_id": str(new_user.inserted_id)}


@router.post("/login")
async def login(user_login: UserLogin):
    user = await users_collection.find_one({"email": user_login.email})
    if not user or not verify_password(user_login.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "status": "success",
        "user_id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"]
    }


@router.get("/users")
async def get_users():
    users = []
    cursor = users_collection.find()
    async for user in cursor:
        user["_id"] = str(user["_id"])
        user.pop("password", None)
        users.append(user)
    return users
