from fastapi import Request, APIRouter
from fastapi.responses import RedirectResponse
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

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
def auth_callback(request: Request):
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
    events_result = service.events().list(
        calendarId='primary',
        maxResults=15,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])


    from app.models.Event import Event
    from dateutil.parser import parse as parse_datetime  # install python-dateutil if needed

    # TEMP USER — replace this with real user logic later
    from app.models.User import User
    temp_user = User(user_id="test69")  # 🔒 Replace with actual user session logic

    for e in events:
        if "dateTime" not in e["start"] or "dateTime" not in e["end"]:
            continue  # skip all-day events for now

        new_event = Event(
            summary=e.get("summary", "Untitled"),
            start_time=parse_datetime(e["start"]["dateTime"]),
            end_time=parse_datetime(e["end"]["dateTime"]),
            notes="Imported from Google"
        )
        temp_user.add_event(new_event)

    ### ✅ Return from the user's calendar object
    return temp_user.get_calendar().to_dict()