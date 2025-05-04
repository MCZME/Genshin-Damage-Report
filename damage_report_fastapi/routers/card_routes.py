from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
from database.crud import CRUD

router = APIRouter(
    prefix="/api",
    tags=["卡片数据"],
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
    "/card-data/random",
    summary="获取随机UID列表",
    description="从MongoDB的analytics集合中随机获取4个UID",
    response_model=Dict[str, Any],
    responses={
        status.HTTP_200_OK: {
            "description": "成功获取随机UID",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "message": "成功",
                        "data": {
                            "uids": ["12345678", "87654321", "11223344", "55667788"]
                        }
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "未找到随机UID数据",
            "content": {
                "application/json": {
                    "example": {
                        "code": 404,
                        "message": "未找到随机UID数据",
                        "data": None
                    }
                }
            }
        }
    }
)
async def get_card_data():
    """
    获取随机UID卡片数据
    
    返回:
        dict: 统一响应格式 {
            "code": 状态码,
            "message": "响应消息",
            "data": {
                "uids": [uid1, uid2, uid3, uid4]
            }
        }
    """
    try:
        uids = await CRUD.get_random_uids()
        if not uids:
            return {
                "code": 404,
                "message": "未找到随机UID数据",
                "data": None
            }
        return {
            "code": 200,
            "message": "成功",
            "data": {
                "uids": uids
            }
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"获取卡片数据失败: {str(e)}",
            "data": None
        }

@router.get(
    "/card-data/{uid}",
    summary="获取指定UID卡片数据", 
    description="通过UID从MongoDB获取卡片详细数据",
    response_model=Dict[str, Any],
    responses={
        status.HTTP_200_OK: {
            "description": "成功获取卡片数据",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "message": "成功",
                        "data": {
                            "name": "队伍名称",
                            "created_at": "2024-05-05T00:00:00",
                            "dps": 50000,
                            "simulation_duration": 90,
                            "team_data": {}
                        }
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "未找到该UID数据",
            "content": {
                "application/json": {
                    "example": {
                        "code": 404,
                        "message": "未找到该UID数据",
                        "data": None
                    }
                }
            }
        }
    }
)
async def get_card_data_by_uid(uid: str):
    """
    获取指定UID卡片详细数据
    
    参数:
        uid: 模拟UID
        
    返回:
        dict: 统一响应格式 {
            "code": 状态码,
            "message": "响应消息",
            "data": {
                "name": 队伍名称,
                "created_at": 创建时间,
                "dps": 伤害数值,
                "simulation_duration": 模拟时长,
                "team_data": 队伍配置数据
            }
        }
    """
    try:
        if not isinstance(uid, str) or not uid:
            raise HTTPException(
                status_code=422,
                detail="UID必须为非空字符串"
            )
            
        analytics_data = await CRUD.get_card_analytics(uid)
        team_data = await CRUD.get_card_config(uid)
        
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
                "team_data": team_data
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取卡片数据失败: {str(e)}"
        )
