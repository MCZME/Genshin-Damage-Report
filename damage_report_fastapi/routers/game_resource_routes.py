from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional
from utils.limiter import limiter
from database.crud import CRUD

router = APIRouter(
    prefix="/api",
    tags=["game_resource"]
)

@router.get("/avatar")
@limiter.limit("200/minute")
async def get_avatar_path(name: str, request: Request):
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
                "code": 200,
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

@router.get("/weapon")
@limiter.limit("200/minute")
async def get_weapon_resource(name: str, request: Request):
    """获取武器资源路径"""
    try:
        path = await CRUD.get_weapon_path(name)
        if not path:
            raise HTTPException(404, detail={
                "code": 404,
                "message": "武器资源不存在",
                "file_path": None
            })
        return JSONResponse(
            content={
                "code": 200,
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

@router.get("/artifact")
@limiter.limit("200/minute")
async def get_artifact_resource(name: str, request: Request):
    """获取圣遗物资源路径"""
    try:
        path = await CRUD.get_artifact_path(name)
        if not path:
            raise HTTPException(404, detail={
                "code": 404,
                "message": "圣遗物资源不存在",
                "file_path": None
            })
        return JSONResponse(
            content={
                "code": 200,
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
