from datetime import datetime
from fastapi import APIRouter, HTTPException
from database.crud import CRUD
from services.data_processing import DataProcessor

router = APIRouter(prefix="/api", tags=["Damage Report"])

@router.get("/health")
async def health_check():
    """健康检查"""
    try:
        await CRUD.find_one("test", {"_id": "health_check"})
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/damage_records")
async def get_damage_records():
    """获取伤害记录"""
    return await CRUD.find_many("damage_records")

@router.post("/damage_records")
async def create_damage_record(record: dict):
    """创建伤害记录"""
    processor = DataProcessor()
    return await processor.process_damage_data(record)

@router.post("/damage_records/batch")
async def batch_create_damage_records(records: list[dict]):
    """批量创建伤害记录"""
    processor = DataProcessor()
    return await processor.batch_process(records)
