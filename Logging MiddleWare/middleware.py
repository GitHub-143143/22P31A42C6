middleware/logging_middleware.py
from fastapi import Request
from datetime import datetime
import json

class LoggingMiddleware:
    """Simple logging middleware for FastAPI"""

    def init(self, app):
        self.app = app

    async def call(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)

            # Create log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown"),
                "content_type": request.headers.get("content-type", "unknown")
            }

            # Log the request
            print(f"[REQUEST] {json.dumps(log_entry, indent=2)}")

        # Continue with the request
        await self.app(scope, receive, send)
