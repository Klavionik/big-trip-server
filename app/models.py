from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Offer(BaseModel):
    id: UUID
    title: str
    price: int


class Activity(BaseModel):
    type: str
    offers: list[Offer]


class Picture(BaseModel):
    description: str
    src: str


class Destination(BaseModel):
    id: UUID
    name: str
    description: str
    pictures: list[Picture]


class EventCreate(BaseModel):
    type: str
    destination: UUID
    date_from: datetime
    date_to: datetime
    offers: list[UUID]
    base_price: int
    is_favorite: bool


class Event(EventCreate):
    id: UUID


class SyncResult(BaseModel):
    updated: list[Event]
