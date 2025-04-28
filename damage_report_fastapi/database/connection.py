from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from mysql.connector import pooling

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
        
    def connect(self, host: str, port: int, user: str, 
                password: str, database: str, pool_size: int = 5):
        """创建MySQL连接池"""
        self.pool = pooling.MySQLConnectionPool(
            pool_name="mysql_pool",
            pool_size=pool_size,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
    def get_connection(self):
        """从连接池获取连接"""
        if not self.pool:
            raise Exception("MySQL连接池未初始化")
        return self.pool.get_connection()
        
    def close(self):
        """关闭所有连接"""
        if self.pool:
            self.pool.closeall()

# 全局数据库实例
db = Database()
mysql_db = MySQLDatabase()
