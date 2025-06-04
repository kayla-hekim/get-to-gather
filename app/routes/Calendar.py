from app.models.event_db import EventDB
from app.database import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/events/save")
async def save_event_to_db(event_data: dict, db: AsyncSession = Depends(get_db)):
    new_event = EventDB(
        user_id="kayla",
        summary=event_data["summary"],
        start_time=event_data["start_time"],
        end_time=event_data["end_time"],
        notes=event_data.get("notes", ""),
        location=event_data.get("location", "")
    )
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return {"event_id": new_event.id}