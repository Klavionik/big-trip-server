from uuid import UUID

import asyncpg.exceptions
from asyncpg import Connection

from app.models import Activity, Destination, Event, EventCreate, SyncResult


async def get_activities(conn: Connection) -> list[Activity]:
    activities = await conn.fetch("SELECT * FROM activities;")
    return [Activity(**row) for row in activities]


async def get_events(conn: Connection) -> list[Event]:
    events = await conn.fetch("SELECT * FROM events;")
    return [Event(**row) for row in events]


async def create_event(event: EventCreate, conn: Connection) -> Event:
    new_id = await conn.fetchval(
        "INSERT INTO events (type, destination, date_from, date_to, offers, base_price, is_favorite) "
        "VALUES ($1, $2, $3, $4, $5, $6, $7)"
        "RETURNING id",
        event.type,
        event.destination,
        event.date_from,
        event.date_to,
        event.offers,
        event.base_price,
        event.is_favorite,
    )
    return Event(id=new_id, **event.model_dump())


async def update_event(event_id: UUID, event: Event, conn: Connection) -> None:
    await conn.execute(
        "UPDATE events SET type = $1, destination = $2, date_from = $3, date_to = $4, offers = $5, "
        "base_price = $6, is_favorite = $7 WHERE id = $8",
        event.type,
        event.destination,
        event.date_from,
        event.date_to,
        event.offers,
        event.base_price,
        event.is_favorite,
        event_id,
    )


async def delete_event(event_id: UUID, conn: Connection) -> None:
    await conn.execute("DELETE FROM events WHERE id = $1;", event_id)


async def get_destinations(conn: Connection) -> list[Destination]:
    destinations = await conn.fetch("SELECT * FROM destinations;")
    return [Destination(**row) for row in destinations]


async def sync_events(events: list[Event], conn: Connection) -> SyncResult:
    result = SyncResult(updated=[])

    for event in events:
        success = False

        try:
            await update_event(event.id, event, conn)
            success = True
        except asyncpg.exceptions.PostgresError:
            pass

        updated_event = SyncResult.UpdatedEvent(
            success=success, payload=SyncResult.UpdatedEvent.Payload(point=event)
        )
        result.updated.append(updated_event)

    return result
