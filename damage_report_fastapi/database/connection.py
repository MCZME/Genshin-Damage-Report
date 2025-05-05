from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from .models import Base

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
        self.engine = None
        self.async_session = None
        
    async def connect(self, host: str, port: int, user: str,
                     password: str, database: str, pool_size: int = 20):
        """创建SQLAlchemy异步引擎和会话工厂"""
        db_url = f"mysql+asyncmy://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_async_engine(
            db_url,
            pool_size=pool_size,
            echo=False
        )
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        
        # 创建所有表(如果不存在)
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def get_session(self):
        """异步上下文管理器获取会话"""
        if not self.async_session:
            raise Exception("SQLAlchemy会话工厂未初始化")
        async with self.async_session() as session:
            yield session
        
# 全局数据库实例
db = Database()
mysql_db = MySQLDatabase()
