from fastapi import APIRouter, HTTPException, Query
from database.crud import CRUD
from typing import Optional

router = APIRouter(prefix="/api", tags=["Sticker"])

@router.get("/stickers/random")
async def get_random_stickers(count: Optional[int] = 25):
    """获取随机表情包
    - count: 返回的表情包数量，默认为25
    """
    try:
        stickers = await CRUD.get_random_stickers(count)
        return {
            "code": 200,
            "message": "success",
            "data": {
                "stickers": stickers
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