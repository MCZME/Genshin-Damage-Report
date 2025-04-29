import time
from fastapi import APIRouter, HTTPException
from database.connection import mysql_db
from typing import Optional

router = APIRouter(prefix="/api", tags=["Sticker"])

@router.get("/stickers/random")
async def get_random_stickers(count: Optional[int] = 25):
    """获取随机表情包
    - count: 返回的表情包数量，默认为25
    """
    try:
        from database.crud import CRUD
        async with CRUD.get_mysql_conn() as conn:
            async with conn.cursor() as cursor:
                # 获取贴纸总数
                await cursor.execute("SELECT COUNT(*) FROM sticker")
                total = (await cursor.fetchone())[0]
                
                if total == 0:
                    return {
                        "code": 200,
                        "message": "success",
                        "data": {
                            "stickers": []
                        }
                    }
                
                # 生成不重复的随机ID列表
                import random
                random_ids = random.sample(range(1, total + 1), min(count, total))
                
                await cursor.execute(
                    "SELECT name, file_name FROM sticker WHERE id IN %s",
                    (tuple(random_ids),)
                )
                result = await cursor.fetchall()
            
            cursor.close()
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "stickers": result
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": 500,
                "message": str(e),
                "data": None
            }
        )
