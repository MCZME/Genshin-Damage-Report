from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from database.crud import CRUD

router = APIRouter(
    prefix="/api",
    tags=["avatar"]
)

@router.get("/avatar")
async def get_avatar_path(name: str):
    """获取角色头像路径"""
    try:
        path = await CRUD.get_avatar_path(name)
        if not path:
            raise HTTPException(404, detail={
                "code": 404,
                "message": "头像不存在",
                "file_path": None
            })
        return JSONResponse(
            content={
                "message": "success",
                "file_path": path
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": 500,
                "message": str(e),
                "file_path": None
            }
        )
