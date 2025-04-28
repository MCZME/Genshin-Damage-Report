from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import asyncmy
from contextlib import asynccontextmanager

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

class MySQLDatabase:
    def __init__(self):
        self.pool = None
        
    async def connect(self, host: str, port: int, user: str,
                     password: str, database: str, pool_size: int = 10):
        """创建异步MySQL连接池"""
        self.pool = await asyncmy.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            minsize=1,
            maxsize=pool_size,
            autocommit=True
        )

    @asynccontextmanager
    async def get_connection(self):
        """异步上下文管理器获取连接"""
        if not self.pool:
            raise Exception("MySQL连接池未初始化")
        async with self.pool.acquire() as conn:
            yield conn

    # 保留同步连接作为fallback
    def sync_connect(self, **kwargs):
        """同步连接方式（兼容旧代码）"""
        return asyncmy.connect(
            host=kwargs['host'],
            port=kwargs['port'],
            user=kwargs['user'],
            password=kwargs['password'],
            database=kwargs['database']
        )
        
# 全局数据库实例
db = Database()
mysql_db = MySQLDatabase()
