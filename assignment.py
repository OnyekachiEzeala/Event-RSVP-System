from fastapi import FastAPI, status, HTTPException, File, UploadFile, Form
from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List, Annotated

app = FastAPI()

class Event(BaseModel):
    id: int
    title: str
    description: str
    date: str
    location: str
    flyer_filename: Optional[str] = None
    rsvps: List[str] = []

class RSVP(BaseModel):
    name: str
    email: str

events: List[Event] = []


# HOME PAGE 
@app.get("/", status_code = status.HTTP_200_OK)
def home():
    return "Welcome to Your Events Homepage"

# POST /events/
@app.post("/events", status_code = status.HTTP_201_CREATED)
def create_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    date: Annotated[str, Form()],
    location: Annotated[str, Form()],
    #optional file uplaod
    flyer: Optional[UploadFile] = File(None)
):
    event_id = len(events) + 1 

    if flyer:
        flyer_filename = flyer.filename
    else:
        flyer_filename = None 

    event = Event (
        id = event_id,
        title = title,
        description = description,
        date = date,
        location = location,
        flyer_filename = flyer_filename,
    )
    events.append(event)
    return {"Message": "Event successfully created", "Data": event}


# GET /events/
@app.get("/events", status_code = status.HTTP_200_OK)
def list_events():
    return events 

# POST /events/{event_id}/rsvp
@app.post("/events/{event_id}/rsvp", status_code = status.HTTP_201_CREATED)
def rsvp_to_event(
    event_id: int, 
    name: Annotated[str, Form()], 
    email: Annotated[str, Form()],
):
    for event in events:
        if event.id == event_id:
            rsvp_details = f"Name: {name}, Email: {email}"
            event.rsvps.append(rsvp_details)
            return f"Congratulations!{name} is attending {event.title}"
    raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = "event not found")






