import logging
from fastapi import Request
from datetime import datetime
from typing import Callable
from fastapi.routing import APIRoute

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/damage_report.log'), 
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MonitoringMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        
        start_time = datetime.now()
        path = scope['path']
        method = scope['method']
        
        logger.info(f"Request started: {method} {path}")
        
        async def wrapped_send(message):
            if message['type'] == 'http.response.start':
                process_time = (datetime.now() - start_time).total_seconds() * 1000
                logger.info(
                    f"Request completed: {method} {path} "
                    f"| Status: {message['status']} "
                    f"| Time: {process_time:.2f}ms"
                )
            await send(message)
            
        await self.app(scope, receive, wrapped_send)

class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            logger.info(f"Endpoint called: {request.url.path}")
            try:
                response = await original_route_handler(request)
                return response
            except Exception as e:
                logger.error(f"Error in {request.url.path}: {str(e)}")
                raise

        return custom_route_handler
