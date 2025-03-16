from collections.abc import AsyncIterator

import orjson
from asyncpg import Connection, connect
from fastapi import Depends

from app.config import Config, get_config


async def get_database(
    config: Config = Depends(get_config),
) -> AsyncIterator[Connection]:
    conn = await connect(str(config.DB_DSN))

    try:
        await conn.set_type_codec(
            "jsonb",
            encoder=lambda *args, **kwargs: orjson.dumps(*args, **kwargs).decode(),
            decoder=lambda *args, **kwargs: orjson.loads(*args, **kwargs).decode(),
            schema="pg_catalog",
        )
        yield conn
    finally:
        await conn.close()
