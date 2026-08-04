from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, DateTime, Boolean, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from starlette import status

from app.db_depends import get_async_db


class Base(DeclarativeBase):
    pass


class EventModel(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime)
    location = Column(String)
    is_active = Column(Boolean, default=True)

from pydantic import BaseModel
from datetime import datetime


class EventSchema(BaseModel):
    id: int
    name: str
    date: datetime
    location: str
    is_active: bool

    class Config:
        from_attributes = True



router = APIRouter(
    prefix="/event",
    tags=["event"]
)

@router.get("/{event_id}", status_code=status.HTTP_200_OK, response_model=EventSchema)
async def get_event(event_id: int, db: AsyncSession = Depends(get_async_db)):
    stmt_event = select(EventModel).where(EventModel.id == event_id, EventModel.is_active == True)
    event = (await db.scalars(stmt_event)).first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event