import contextlib
from collections.abc import AsyncIterator
from typing import TypedDict

from asyncpg import Pool, create_pool
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import router
from app.config import get_config


class State(TypedDict):
    db_pool: Pool


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[State]:
    config = get_config()

    async with create_pool(str(config.DB_DSN), min_size=1, max_size=5) as pool:
        yield {"db_pool": pool}


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    @app.get("/healthz")
    async def healthz() -> str:
        return "OK"

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_credentials=True
    )
    return app
