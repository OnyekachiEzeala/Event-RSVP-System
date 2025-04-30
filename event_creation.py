from typing import Annotated, Optional

from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from uuid import UUID

app = FastAPI()


class EventBase(BaseModel):
  title: Annotated[str, Form()]
  description: Annotated[str, Form()]
  date: Annotated[str, Form()]
  location: Annotated[str, Form()]
  flyer_name: Optional[UploadFile] = File(None)
  # rsvp: list[Annotated[str, Form()]]

class Event(EventBase):
  id: int

events: list[EventBase] = []

@app.post("/events/")
async def event(
  title: Annotated[str, Form()],
  description: Annotated[str, Form()],
  date: Annotated[str, Form()],
  location: Annotated[str, Form()],
  flyer_name: Optional[UploadFile] = File(None)
):
  event_id =str(UUID(int=len(events) + 1))
  events.append(Event)
  
  
  item_data = {
    "id":  event_id,
    "title": title,
    "description": description,
    "date": date,
    "location": location,
    "flyer_name": flyer_name.filename
  }
  
  return {"Message" : "Event created successfully!", "event_data" : item_data}