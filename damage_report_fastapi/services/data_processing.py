from datetime import datetime
from typing import Any, Dict, List
from fastapi import HTTPException
from ..database import crud

class DataProcessor:
    def __init__(self):
        self.crud = crud.CRUD()

    async def process_damage_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理伤害数据"""
        try:
            # 数据验证
            if not all(key in data for key in ['character', 'damage', 'timestamp']):
                raise ValueError("Missing required fields")
            
            # 数据处理逻辑
            processed_data = {
                'character': data['character'],
                'damage': float(data['damage']),
                'timestamp': data['timestamp'],
                'processed_at': datetime.now().isoformat()
            }
            
            # 保存到数据库
            await self.crud.create_damage_record(processed_data)
            
            return processed_data
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

    async def batch_process(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量处理伤害数据"""
        return [await self.process_damage_data(data) for data in data_list]
