from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
from database.crud import CRUD

router = APIRouter(
    prefix="/api",
    tags=["角色数据"],
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
    "/character/element",
    summary="获取角色元素类型",
    description="通过角色名称从MongoDB获取角色元素类型",
    response_model=Dict[str, Any],
    responses={
        status.HTTP_200_OK: {
            "description": "成功获取角色元素类型",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "message": "成功",
                        "data": {
                            "element": "火",
                            "name": "胡桃"
                        }
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "未找到该角色数据",
            "content": {
                "application/json": {
                    "example": {
                        "code": 404,
                        "message": "未找到该角色数据",
                        "data": None
                    }
                }
            }
        }
    }
)
async def get_character_element(name: str):
    """
    获取指定角色元素类型
    
    参数:
        name: 角色名称
        
    返回:
        dict: 统一响应格式 {
            "code": 状态码,
            "message": "响应消息",
            "data": {
                "element": 元素类型,
                "name": 角色名称
            }
        }
    """
    try:
        if not isinstance(name, str) or not name:
            raise HTTPException(
                status_code=422,
                detail="角色名称必须为非空字符串"
            )
            
        element = await CRUD.get_element_by_name(name)
        
        if not element:
            raise HTTPException(
                status_code=404,
                detail="未找到该角色相关数据"
            )
            
        return {
            "code": 200,
            "message": "成功",
            "data": {
                "element": element,
                "name": name
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取角色数据失败: {str(e)}"
        )