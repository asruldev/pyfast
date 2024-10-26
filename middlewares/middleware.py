from time import time
from fastapi.requests import Request
import logging

# Middleware logging
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logging.info(f"Request: {request.url} | Status code: {response.status_code}")
    return response

# Middleware waktu proses
async def add_latency_to_response(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.3f}ms"
    return response