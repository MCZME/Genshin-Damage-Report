from .connection import db, mysql_db
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

class CRUD:
    @staticmethod
    @asynccontextmanager
    async def get_mysql_conn():
        """获取MySQL异步连接"""
        async with mysql_db.get_connection() as conn:
            yield conn

    @staticmethod
    async def create_damage_report(report_data: Dict[str, Any]):
        """创建损害报告（MySQL）"""
        async with CRUD.get_mysql_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO damage_reports (title, description) VALUES (%s, %s)",
                    (report_data['title'], report_data['description'])
                )
                await conn.commit()
                return cursor.lastrowid

    @staticmethod
    async def get_damage_report(report_id: int):
        """获取损害报告（MySQL）"""
        async with CRUD.get_mysql_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT * FROM damage_reports WHERE id = %s",
                    (report_id,)
                )
                return await cursor.fetchone()
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

    @staticmethod
    async def get_avatar_path(character_name: str):
        """获取角色头像路径"""
        async with CRUD.get_mysql_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT file_path FROM avatar WHERE name = %s",
                    (character_name,)
                )
                result = await cursor.fetchone()
                return result[0] if result else None

    @staticmethod
    async def get_weapon_path(weapon_name: str):
        """获取武器图片路径"""
        async with CRUD.get_mysql_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT file_path FROM weapon WHERE name = %s",
                    (weapon_name,)
                )
                result = await cursor.fetchone()
                return result[0] if result else None

    @staticmethod
    async def get_artifact_path(artifact_name: str):
        """获取圣遗物图片路径"""
        async with CRUD.get_mysql_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT file_path FROM artifact WHERE name = %s",
                    (artifact_name,)
                )
                result = await cursor.fetchone()
                return result[0] if result else None
