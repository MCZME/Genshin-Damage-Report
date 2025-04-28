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
        conn = mysql_db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT name, file_name FROM `sticker` ORDER BY RAND() LIMIT %s"
        cursor.execute(query, (count,))
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
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
