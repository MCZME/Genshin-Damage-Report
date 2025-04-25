from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import Dict, Optional
import re

class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window  # seconds
        self.request_logs: Dict[str, list] = {}

    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        now = datetime.now()
        
        if client_ip not in self.request_logs:
            self.request_logs[client_ip] = []
        
        # 清理过期的请求记录
        self.request_logs[client_ip] = [
            t for t in self.request_logs[client_ip] 
            if now - t < timedelta(seconds=self.window)
        ]
        
        # 检查请求频率
        if len(self.request_logs[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429, 
                detail=f"Too many requests. Limit is {self.max_requests} per minute"
            )
        
        self.request_logs[client_ip].append(now)

class SecurityMiddleware:
    def __init__(self, app):
        self.app = app
        self.rate_limiter = RateLimiter()

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        
        request = Request(scope, receive)
        
        # 检查请求频率
        try:
            await self.rate_limiter.check_rate_limit(request)
        except HTTPException as e:
            return await send({
                'type': 'http.response.start',
                'status': e.status_code,
                'headers': [(b'content-type', b'application/json')]
            })
        
        # 添加安全头部
        async def wrapped_send(message):
            if message['type'] == 'http.response.start':
                headers = dict(message.get('headers', []))
                headers.update({
                    b'X-Content-Type-Options': b'nosniff',
                    b'X-Frame-Options': b'DENY',
                    b'X-XSS-Protection': b'1; mode=block',
                    b'Content-Security-Policy': b"default-src 'self'"
                })
                message['headers'] = list(headers.items())
            await send(message)
            
        await self.app(scope, receive, wrapped_send)

def sanitize_input(data: str) -> Optional[str]:
    """清理用户输入，防止XSS攻击"""
    if not data:
        return None
    # 移除危险字符和标签
    cleaned = re.sub(r'<[^>]*>', '', data)
    cleaned = re.sub(r'[\'\";]', '', cleaned)
    return cleaned.strip()
