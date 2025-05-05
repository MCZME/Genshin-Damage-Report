from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
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
async def get_character_element(teamMember: List[str] = Query(...)):
    """
    批量获取角色元素类型
    
    参数:
        teamMember: 角色名称列表
        
    返回:
        dict: 统一响应格式 {
            "code": 状态码,
            "message": "响应消息",
            "data": [
                {
                    "element": 元素类型,
                    "name": 角色名称
                },
                ...
            ]
        }
    """
    try:
        if not isinstance(teamMember, list) or not teamMember:
            raise HTTPException(
                status_code=422,
                detail="请求参数错误: teamMember 应为非空列表"
            )
            
        elements = await CRUD.get_elements_by_names(teamMember)
        
        if not elements:
            raise HTTPException(
                status_code=404,
                detail="未找到相关角色数据"
            )
            
        return {
            "code": 200,
            "message": "成功",
            "data": [
                {"name": name, "element": element}
                for name, element in elements.items()
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取角色数据失败: {str(e)}"
        )
