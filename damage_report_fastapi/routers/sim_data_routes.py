from fastapi import APIRouter, HTTPException, Request, status
from typing import List, Dict, Any

from database.crud import CRUD
from utils.limiter import limiter

router = APIRouter(
    prefix="/api",
    tags=["模拟数据"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "服务器内部错误",
            "content": {
                "application/json": {
                    "example": {
                        "code": 500,
                        "message": "服务器内部错误",
                        "data": None
                    }
                }
            }
        }
    }
)

@router.get(
    '/sim-data/{uid}',
    summary="获取模拟数据",
    description="根据UID获取模拟数据",
    response_model=Dict[str, Any],
    responses={
        status.HTTP_200_OK: {
            "description": "成功获取模拟数据",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "message": "成功",
                        "data": {
                            "uuid": "12345678",
                            "data": {
                                # 模拟数据内容
                            }
                        }
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "未找到模拟数据",
            "content": {
                "application/json": {
                    "example": {
                        "code": 404,
                        "message": "未找到模拟数据",
                        "data": None
                    }
                }
            }
        }
    }
)
@limiter.limit("10/minute")
async def get_sim_result(uid: str, request: Request):
    """
    获取模拟数据

    参数:
        uid (str): 模拟数据的UID

    返回:
        dict: 包含模拟数据的字典
    """
    if not isinstance(uid, str) or not uid:
            raise HTTPException(
                status_code=422,
                detail="UID必须为非空字符串"
            )
    
    try:
        analytics_data = await CRUD.get_sim_result(uid)
        team_data = await CRUD.get_team_config(uid)
        
        if not analytics_data and not team_data:
            raise HTTPException(
                status_code=404,
                detail="未找到该UID相关数据"
            )
            
        return {
            "code": 200,
            "message": "成功",
            "data": {
                **analytics_data,
                **team_data
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取卡片数据失败: {str(e)}"
        )
