from typing import Annotated, Optional
from datetime import datetime,date
from fastapi import FastAPI, File, UploadFile, Form, status, HTTPException
from pydantic import BaseModel
from uuid import UUID

app = FastAPI()


class EventBase(BaseModel):
  title: str
  description: str
  location: str
  date : date
  # flyer: Optional[Annotated[UploadFile, Form()]]
  # rsvp: list[Annotated[str, Form()]]

class Event(EventBase):
  pass

events: list[EventBase] = []

# =======Post an Event=======
@app.post("/events" , status_code=status.HTTP_201_CREATED)
async def create_event(event : Annotated[Event, Form()]):
  event_dict = event.model_dump()
  event_dict['id'] = len(events) + 1
  event_dict['event_create_at'] = datetime.now()
  events.append(event_dict)
  return event_dict

# =========Listing the Events======
@app.get("/events", status_code=status.HTTP_200_OK)
async def list_event():
  if not events:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  return events
