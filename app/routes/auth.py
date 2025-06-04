from fastapi import Request, APIRouter
from fastapi.responses import RedirectResponse
from app.data.Users import get_or_create_user
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from app.data.Users import get_or_create_user
from app.models.User import User
from app.models.Event import Event
from dateutil.parser import parse as parse_datetime

from app.models.event_db import EventDB
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from dateutil.parser import parse as parse_datetime
from sqlalchemy.future import select
from sqlalchemy import and_

from app.models.user_db import UserDB
from app.models.calendar_db import CalendarDB




router = APIRouter()


# Absolute path to your client_secret.json (adjust as needed)
GOOGLE_CLIENT_SECRETS_FILE = "/Users/kaylakim/Downloads/get_to_gather/get-to-gather/app/routes/client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
REDIRECT_URI = "http://localhost:8000/auth/callback"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # only for testing (http)


@router.get("/auth/login")
def login():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return RedirectResponse(auth_url)


@router.get("/auth/callback")
async def auth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    code = request.query_params.get("code")
    
    # This flow must match the one used during login
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    flow.fetch_token(code=code)
    credentials = flow.credentials

    service = build("calendar", "v3", credentials=credentials)
    
    profile_info = service.calendarList().get(calendarId='primary').execute()
    google_email = profile_info.get("id", "unknown_user")

    result = await db.execute(select(UserDB).where(UserDB.email == google_email))
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        new_user = UserDB(email=google_email)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)  # gets new_user.user_id
        user_id = new_user.id
    else:
        user_id = existing_user.id

    user_info = service.settings().get(setting='timezone').execute()  # simple API call just to test access
    # you can later use Google People API to get full name

    # Save user
    await get_or_create_user(db, user_id)

    events_result = service.events().list(
        calendarId='primary',
        maxResults=15,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    from app.models.calendar_db import CalendarDB

    result = await db.execute(select(CalendarDB).where(CalendarDB.user_id == user_id))
    calendar = result.scalar_one_or_none()

    if not calendar:
        calendar = CalendarDB(user_id=user_id)
        db.add(calendar)
        await db.commit()
        await db.refresh(calendar)


    # temp_user = User(user_id="test69")
    # user = get_or_create_user("kayla")

    saved = 0
    for e in events:
        if "dateTime" not in e["start"] or "dateTime" not in e["end"]:
            continue  # skip all-day events

        exists_query = await db.execute(
            select(EventDB).where(
                and_(
                    EventDB.summary == e.get("summary", "Untitled"),
                    EventDB.start_time == parse_datetime(e["start"]["dateTime"])
                )
            )
        )
        existing = exists_query.scalar_one_or_none()

        if existing:
            continue  # skip duplicates

        new_event = EventDB(
            calendar_id=calendar.id,
            summary=e.get("summary", "Untitled"),
            start_time=parse_datetime(e["start"]["dateTime"]),
            end_time=parse_datetime(e["end"]["dateTime"]),
            notes="Imported from Google",
            location=e.get("location", "")
        )
        db.add(new_event)
        saved += 1

    await db.commit()

    return RedirectResponse(url=f"http://localhost:3000/calendar/{user_id}")


@router.get("/calendar/{user_id}")
async def get_user_calendar(user_id: int, db: AsyncSession = Depends(get_db)):
    calendar_result = await db.execute(
        select(CalendarDB.id).where(CalendarDB.user_id == user_id)
    )
    calendar_ids = [row[0] for row in calendar_result.all()]

    if not calendar_ids:
        return {"events": []}

    result = await db.execute(
        select(EventDB).where(EventDB.calendar_id.in_(calendar_ids))
    )
    events = result.scalars().all()

    return {
        "events": [
            {
                "summary": e.summary,
                "start": e.start_time.isoformat(),
                "end": e.end_time.isoformat(),
                "location": e.location,
                "notes": e.notes
            }
            for e in events
        ]
    }