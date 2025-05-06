from .connection import db, mysql_db
from .models import Avatar, Weapon, Artifact, Character, Sticker
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
from sqlalchemy import select, func
import random

class CRUD:
    @staticmethod
    @asynccontextmanager
    async def get_session():
        """获取SQLAlchemy异步会话"""
        async with mysql_db.get_session() as session:
            yield session

    @staticmethod
    async def get_avatar_path(character_name: str):
        """获取角色头像路径"""
        async with CRUD.get_session() as session:
            result = await session.execute(
                select(Avatar.file_path)
                .where(Avatar.name == character_name)
            )
            avatar = result.scalar_one_or_none()
            return avatar

    @staticmethod
    async def get_weapon_path(weapon_name: str):
        """获取武器图片路径"""
        async with CRUD.get_session() as session:
            result = await session.execute(
                select(Weapon.file_path)
                .where(Weapon.name == weapon_name)
            )
            weapon = result.scalar_one_or_none()
            return weapon

    @staticmethod
    async def get_artifact_path(artifact_name: str):
        """获取圣遗物图片路径"""
        async with CRUD.get_session() as session:
            result = await session.execute(
                select(Artifact.file_path)
                .where(Artifact.name == artifact_name)
            )
            artifact = result.scalar_one_or_none()
            return artifact

    @staticmethod
    async def get_random_stickers(count: int = 25) -> list[dict]:
        """获取随机表情包"""
        async with CRUD.get_session() as session:
            # 获取总数
            total = await session.scalar(select(func.count()).select_from(Sticker))
            
            if total == 0:
                return []
                
            # 生成随机偏移量
            offset = random.randint(0, max(0, total - count))
            
            # 查询随机范围的表情包
            result = await session.execute(
                select(Sticker)
                .offset(offset)
                .limit(count)
            )
            stickers = result.scalars().all()
            return [{
                "name": s.name,
                "file_name": s.file_name,
            } for s in stickers]
        
    @staticmethod
    async def get_elements_by_names(names: list[str]) -> dict:
        """批量获取角色元素类型"""
        async with CRUD.get_session() as session:
            result = await session.execute(
                select(Character.name, Character.element)
                .where(Character.name.in_(names))
            )
            elements = {row[0]: row[1] for row in result.all()}
            return elements

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
    async def get_team_config(uid: str) -> dict:
        """从configs集合获取队伍配置"""
        if db.db is None:
            raise ValueError("MongoDB数据库未连接")
            
        doc = await db.db.configs.find_one(
            {"uid": uid}, 
            {"_id":0, "team_data":1, "action_sequence":1, "target_data":1}
        )
        return doc if doc else {}
    
    @staticmethod
    async def get_sim_result(uid: str) -> dict:
        """通过UID获取模拟结果分析数据"""
        if db.db is None:
            raise ValueError("MongoDB数据库未连接")
            
        doc = await db.db.analytics.find_one(
            {"uid": uid}, 
            {"_id":0, "name":1, "created_at":1, "dps":1, "simulation_duration":1, "frames":1}
        )
        return doc or {}
