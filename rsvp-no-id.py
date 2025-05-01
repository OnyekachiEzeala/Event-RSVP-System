from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import os

# Initialize the FastAPI app
app = FastAPI()

# Data storage (acting as our "database")
events = []
rsvps = {}

# Create a folder for uploaded flyers if it doesn't exist
os.makedirs("flyers", exist_ok=True)

# Schemas
class Event(BaseModel):
    id: int
    title: str
    description: str
    date: date
    location: str
    flyer_filename: Optional[str] = None

class RSVP(BaseModel):
    name: str
    email: str

# 1. Create a new event
@app.post("/events/")
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: date = Form(...),
    location: str = Form(...),
    flyer: Optional[UploadFile] = File(None)
):
    event_id = len(events) + 1  # Auto-increment event ID

    flyer_filename = None
    if flyer:
        flyer_filename = flyer.filename
        flyer_path = f"flyers/{flyer.filename}"
        with open(flyer_path, "wb") as f:
            f.write(await flyer.read())

    event = Event(
        id=event_id,
        title=title,
        description=description,
        date=date,
        location=location,
        flyer_filename=flyer_filename
    )
    events.append(event)
    rsvps[event_id] = []  # Initialize empty RSVP list for this event

    return {"message": "Event created successfully", "event_id": event_id}

# 2. List all events (with optional filtering by location)
@app.get("/events/", response_model=List[Event])
async def list_events(location: Optional[str] = None):
    if location:
        return [event for event in events if event.location.lower() == location.lower()]
    return events

# 3. RSVP to an event
@app.post("/events/{event_id}/rsvp")
async def rsvp_event(
    event_id: int,
    name: str = Form(...),
    email: str = Form(...)
):
    if event_id not in rsvps:
        raise HTTPException(status_code=404, detail="Event not found")

    rsvp = RSVP(name=name, email=email)
    rsvps[event_id].append(rsvp)

    return {"message": "RSVP successful"}

# 4. List RSVPs for an event
@app.get("/events/{event_id}/rsvps", response_model=List[RSVP])
async def list_rsvps(event_id: int):
    if event_id not in rsvps:
        raise HTTPException(status_code=404, detail="Event not found")
    return rsvps[event_id]
