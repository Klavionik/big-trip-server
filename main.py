from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("/activities")
async def get_activities():
    pass


@router.get("/events")
async def get_events():
    pass


@router.post("/events")
async def create_event():
    pass


@router.put("/events/{event_id}")
async def update_event(event_id: int):
    pass


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    pass


@router.get("/destinations")
async def get_destinations():
    pass


@router.post("/events/sync")
async def sync_events():
    pass
