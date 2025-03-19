from uuid import UUID

from asyncpg import Connection
from fastapi import APIRouter, Depends

from app import crud
from app.deps import get_database
from app.models import Activity, Destination, Event, EventCreate, SyncResult

router = APIRouter(prefix="/api/v1")


@router.get("/activities")
async def get_activities(conn: Connection = Depends(get_database)) -> list[Activity]:
    return await crud.get_activities(conn)


@router.get("/events")
async def get_events(conn: Connection = Depends(get_database)) -> list[Event]:
    return await crud.get_events(conn)


@router.post("/events", status_code=201)
async def create_event(
    event: EventCreate, conn: Connection = Depends(get_database)
) -> Event:
    return await crud.create_event(event, conn)


@router.put("/events/{event_id}")
async def update_event(
    event_id: UUID, event: Event, conn: Connection = Depends(get_database)
) -> Event:
    await crud.update_event(event_id, event, conn)
    return event


@router.delete("/events/{event_id}", status_code=204)
async def delete_event(
    event_id: UUID, conn: Connection = Depends(get_database)
) -> None:
    await crud.delete_event(event_id, conn)


@router.get("/destinations")
async def get_destinations(
    conn: Connection = Depends(get_database),
) -> list[Destination]:
    return await crud.get_destinations(conn)


@router.post("/events/sync")
async def sync_events(
    events: list[Event], conn: Connection = Depends(get_database)
) -> SyncResult:
    return await crud.sync_events(events, conn)
