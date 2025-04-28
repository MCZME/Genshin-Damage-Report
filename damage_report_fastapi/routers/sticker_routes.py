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
        with mysql_db.connection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            # 获取贴纸总数
            cursor.execute("SELECT COUNT(*) as total FROM `sticker`")
            total = cursor.fetchone()['total']
            
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
            random_ids = random.sample(range(1, total + 1), min(count, total))  # sample保证不重复
            
            # 查询随机ID对应的贴纸
            query = f"SELECT name, file_name FROM `sticker` WHERE id IN {tuple(random_ids)}"
            cursor.execute(query)
            result = cursor.fetchall()
            
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
