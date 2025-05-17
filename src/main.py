from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import settings.logger
from settings.redis import get_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.logger.configure_logger()
    redis_client = get_redis_client()
    yield
    await redis_client.close()

app = FastAPI(lifespan=lifespan)

origins = ["http://127.0.0.1:8000", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

