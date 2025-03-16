import asyncio

import typer
from asyncpg import connect
from pydantic import TypeAdapter

from app.config import get_config
from app.models import Activity, Destination, Offer, Picture

app = typer.Typer()

Activities = TypeAdapter(list[Activity])
Destinations = TypeAdapter(list[Destination])
Offers = TypeAdapter(list[Offer])
Pictures = TypeAdapter(list[Picture])


@app.callback()
def callback() -> None:
    pass


@app.command()
def provision() -> None:
    config = get_config()

    async def _provision() -> None:
        with (
            open("fixtures/activities.json") as fh_a,
            open("fixtures/destinations.json") as fh_d,
        ):
            activities = Activities.validate_json(fh_a.read())
            destinations = Destinations.validate_json(fh_d.read())

        conn = await connect(str(config.DB_DSN))

        try:
            async with conn.transaction():
                await conn.execute("TRUNCATE activities;")
                await conn.execute("TRUNCATE destinations CASCADE;")

                for activity in activities:
                    await conn.execute(
                        "INSERT INTO activities (type, offers) VALUES ($1, $2)",
                        activity.type,
                        Offers.dump_json(activity.offers).decode(),
                    )

                for destination in destinations:
                    await conn.execute(
                        "INSERT INTO destinations (id, name, description, pictures) VALUES ($1, $2, $3, $4)",
                        destination.id,
                        destination.name,
                        destination.description,
                        Pictures.dump_json(destination.pictures).decode(),
                    )
        finally:
            await conn.close()

    asyncio.run(_provision())


@app.command()
def migrate() -> None:
    config = get_config()

    async def _migrate() -> None:
        conn = await connect(str(config.DB_DSN))

        try:
            async with conn.transaction():
                await conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS activities (
                        type TEXT PRIMARY KEY,
                        offers JSONB NOT NULL
                    );
                    """
                )
                await conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS destinations (
                        id UUID PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        pictures JSONB NOT NULL
                    );
                    """
                )
                await conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS events (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        type TEXT NOT NULL,
                        destination UUID REFERENCES destinations (id),
                        date_from TIMESTAMP WITH TIME ZONE NOT NULL,
                        date_to TIMESTAMP WITH TIME ZONE NOT NULL,
                        offers JSONB NOT NULL,
                        base_price BIGINT NOT NULL,
                        is_favorite BOOLEAN NOT NULL
                    );
                    """
                )
        finally:
            await conn.close()

    asyncio.run(_migrate())


if __name__ == "__main__":
    app()
