from collections.abc import AsyncIterator

import orjson
from asyncpg import Connection
from fastapi import Request


async def get_database(
    request: Request,
) -> AsyncIterator[Connection]:
    async with request.state.db_pool.acquire() as conn:
        await conn.set_type_codec(
            "jsonb",
            encoder=lambda *args, **kwargs: orjson.dumps(*args, **kwargs).decode(),
            decoder=orjson.loads,
            schema="pg_catalog",
        )
        yield conn
