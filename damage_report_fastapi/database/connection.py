from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

class Database:
    def __init__(self):
        self.async_client = None
        self.sync_client = None
        
    async def connect(self, uri: str, db_name: str):
        """异步连接MongoDB"""
        self.async_client = AsyncIOMotorClient(uri)
        self.sync_client = MongoClient(uri)
        self.db = self.async_client[db_name]
        self.sync_db = self.sync_client[db_name]
        return self.db
        
    async def close(self):
        """关闭数据库连接"""
        if self.async_client:
            self.async_client.close()
        if self.sync_client:
            self.sync_client.close()

# 全局数据库实例
db = Database()
