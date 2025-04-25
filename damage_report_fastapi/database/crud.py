from .connection import db
from typing import Optional, Dict, Any

class CRUD:
    @staticmethod
    async def insert_one(collection: str, document: Dict[str, Any]):
        """插入单个文档"""
        return await db.db[collection].insert_one(document)

    @staticmethod
    async def find_one(collection: str, query: Dict[str, Any]):
        """查询单个文档"""
        return await db.db[collection].find_one(query)

    @staticmethod
    async def update_one(collection: str, query: Dict[str, Any], update: Dict[str, Any]):
        """更新单个文档"""
        return await db.db[collection].update_one(query, {"$set": update})

    @staticmethod
    async def delete_one(collection: str, query: Dict[str, Any]):
        """删除单个文档"""
        return await db.db[collection].delete_one(query)

    @staticmethod
    async def find_many(collection: str, query: Optional[Dict[str, Any]] = None):
        """查询多个文档"""
        query = query or {}
        cursor = db.db[collection].find(query)
        return [doc async for doc in cursor]
