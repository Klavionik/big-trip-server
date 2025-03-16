from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    @app.get("/healthz")
    async def healthz() -> str:
        return "OK"

    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_credentials=True
    )
    return app
