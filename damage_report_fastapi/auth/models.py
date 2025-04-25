from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from database.connection import db

class User(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    role: str = "user"
    created_at: datetime = datetime.now()
    last_login: Optional[datetime] = None

    @classmethod
    async def get_collection(cls):
        return await db.get_collection("users")

    @classmethod 
    async def find_by_username(cls, username: str) -> Optional["User"]:
        collection = await cls.get_collection()
        user_data = await collection.find_one({"username": username})
        return cls(**user_data) if user_data else None

    @classmethod
    async def create_user(cls, user_data: dict) -> "User":
        collection = await cls.get_collection()
        result = await collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return cls(**user_data)
