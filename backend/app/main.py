import os
from datetime import datetime
from fastapi import Depends, FastAPI, Request

from app.dependencies import get_query_token

from app.routers import user
import logging
import sys
from contextlib import asynccontextmanager

from app.config import settings
from app.utils.database import sessionmanager

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.debug_logs else logging.INFO)


lifespan = None
init_db = True

if init_db:
    sessionmanager.init(settings.DATABASE_URL)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        if sessionmanager._engine is not None:
            await sessionmanager.close()

app = FastAPI(title="FastAPI server", lifespan=lifespan)


async def request_timing_middleware(request: Request, call_next: Request):
    start_time = datetime.now()  # Capture start time at the beginning
    response = await call_next(request)
    processing_time = datetime.now() - start_time
    # Log request processing time (replace with your logging library)
    print(f"Request {request.url.path} processed in {processing_time}")
    return response

app.middleware("http")(request_timing_middleware)  # Apply to all HTTP requests

app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}