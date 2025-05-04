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

    @staticmethod
    async def get_random_uids(count: int = 4) -> list[str]:
        """从MongoDB的analytics集合获取随机uid列表"""
        try:
            if db.db is None:
                raise ValueError("MongoDB数据库未连接")
                
            pipeline = [
                {"$sample": {"size": count}},
                {"$project": {"_id": 0, "uid": 1}}
            ]
            cursor = db.db.analytics.aggregate(pipeline)
            return [doc["uid"] async for doc in cursor]
        except Exception as e:
            print(f"获取随机uid失败: {e}")
            return []

    @staticmethod
    async def get_card_analytics(uid: str) -> dict:
        """从analytics集合获取卡片基础数据"""
        if db.db is None:
            raise ValueError("MongoDB数据库未连接")
            
        doc = await db.db.analytics.find_one(
            {"uid": uid}, 
            {"_id":0, "name":1, "created_at":1, "dps":1, "simulation_duration":1}
        )
        return doc or {}

    @staticmethod
    async def get_card_config(uid: str) -> dict:
        """从configs集合获取队伍配置"""
        if db.db is None:
            raise ValueError("MongoDB数据库未连接")
            
        doc = await db.db.configs.find_one(
            {"uid": uid}, 
            {"_id":0, "team_data":1}
        )
        return doc.get("team_data", {}) if doc else {}

    @staticmethod
    async def get_element_by_name(name: str):
        """通过角色名获取角色元素"""
        async with CRUD.get_mysql_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT Element FROM `character` WHERE name = %s",
                    (name,)
                )
                result = await cursor.fetchone()
                return result[0] if result else None
