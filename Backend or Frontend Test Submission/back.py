from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, HttpUrl, validator
from datetime import datetime, timedelta
import string
import random
import uvicorn
from typing import Optional, Dict, Any, List
import json
import re
import ipaddress
class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now()

        log_data = {
            "timestamp": start_time.isoformat(),
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", "unknown"),
            "referer": request.headers.get("referer", "direct"),
            "content_type": request.headers.get("content-type", "unknown"),
            "host": request.headers.get("host", "unknown")
        }

        print(f"[REQUEST] {json.dumps(log_data, indent=2)}")

        response = await call_next(request)

        response_log = {
            "timestamp": datetime.now().isoformat(),
            "status_code": response.status_code,
            "processing_time_ms": (datetime.now() - start_time).total_seconds() * 1000,
            "path": request.url.path,
            "method": request.method
        }
        print(f"[RESPONSE] {json.dumps(response_log, indent=2)}")

        return response

    def _get_client_ip(self, request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        return request.client.host if request.client else "unknown"
