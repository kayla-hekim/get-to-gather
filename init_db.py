import asyncio
from app.database import engine, Base
from app.models.event_db import EventDB
from app.models.user_db import UserDB
from app.models.calendar_db import CalendarDB

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init())