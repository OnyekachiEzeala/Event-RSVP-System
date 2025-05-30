from typing import Annotated, List, Optional
from datetime import datetime,date
from fastapi import FastAPI, File, UploadFile, Form, status, HTTPException, Depends
from pydantic import BaseModel
from uuid import UUID

app = FastAPI()


class EventBase(BaseModel):
    title: str
    description: str
    location: str
    id: int
    event_create_at: datetime
    date: date
    flyer: Optional[str] = None  # Store filename as string
    rsvp: List[str] = []

class Event(EventBase):
  pass

class RSVP(BaseModel):
  name: str
  email: str


events: list[EventBase] = []



# =======Post an Event=======
@app.post("/events", status_code=status.HTTP_201_CREATED)
async def create_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    location: Annotated[str, Form()],
    date: Annotated[date, Form()],
    flyer: Optional[UploadFile] = File(None),
    rsvp: Annotated[List[str], Form()] = []
):
    # Create a new event
    # event data is used to create a new event in dictionary
    # flyer is an optional file upload
    # flyer.filename is used to store the filename
    event_data = {
        "title": title,
        "description": description,
        "location": location,
        "date": date,
        "rsvp": rsvp,
        "flyer": flyer.filename if flyer is not None else None,
        "id": len(events) + 1,
        "event_create_at": datetime.now()
    }
     
    # Add to events list
    events.append(event_data)
    
    # Return the created event
    return event_data

# =========Listing the Events======
@app.get("/events", status_code=status.HTTP_200_OK)
async def list_event():
  if not events:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  return events

# ========Get Events by ID========
@app.get ("/events/{event_id}", status_code = status.HTTP_200_OK)
def get_event_by_id(event_id:int):
    for event in events:
        if event["id"] == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")


@app.post("/events/{event_id}/rsvp", status_code=status.HTTP_201_CREATED)
async def rsvp_event(event_id:int, response: Annotated[RSVP, Form()]):
  for event in events:
    if event["id"] == event_id:
        rsvp_data = response.model_dump()
        if "rsvp" not in event:
           event["rsvp"] = []
        event["rsvp"].append(rsvp_data)
        return {
            "message": f"RSVP received for event {event_id}",
            "rsvp": response,
        }
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")


@app.get("/events/{event_id}/rsvps", status_code=status.HTTP_200_OK)
def list_rsvps(event_id:int):
   for event in events:
      if event["id"] == event_id:
         return event.get("rsvp", [])
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Event not found')