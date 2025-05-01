from typing import List, Dict
from datetime import datetime, date
from fastapi import FastAPI, Form, status, HTTPException
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

# ==== Pydantic Models ====

class EventBase(BaseModel):
    title: str
    description: str
    location: str
    date: date

class Event(EventBase):
    id: str
    created_at: datetime

class RSVP(BaseModel):
    name: str
    email: str


# ==== In-memory "database" ====
events: List[Event] = []
rsvps: Dict[str, List[RSVP]] = {}

# ==== Create Event (POST /events) ====
@app.post("/events", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    date: date = Form(...)
):
    event_id = str(uuid4())
    new_event = Event(
        id=event_id,
        title=title,
        description=description,
        location=location,
        date=date,
        created_at=datetime.now()
    )
    events.append(new_event)
    rsvps[event_id] = []  # Initialize empty RSVP list
    return new_event

# ==== List All Events (GET /events) ====
@app.get("/events", response_model=List[Event])
async def list_events():
    if not events:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return events

# ==== RSVP to an Event (POST /events/{event_id}/rsvp) ====
@app.post("/events/{event_id}/rsvp", status_code=status.HTTP_201_CREATED)
async def rsvp_event(event_id: str, name: str = Form(...), email: str = Form(...)):
    if event_id not in rsvps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    rsvp = RSVP(name=name, email=email)
    rsvps[event_id].append(rsvp)
    return {"message": "RSVP successful", "rsvp": rsvp}

# ==== List RSVPs for an Event (GET /events/{event_id}/rsvps) ====
@app.get("/events/{event_id}/rsvps", response_model=List[RSVP])
async def get_rsvps(event_id: str):
    if event_id not in rsvps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return rsvps[event_id]
