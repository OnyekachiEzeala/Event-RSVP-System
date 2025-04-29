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
  # flyer: Optional[Annotated[UploadFile, Form()]]
  # rsvp: list[Annotated[str, Form()]]

class Event(EventBase):
  id: int

events: list[Event] = []

@app.post("/event/")
async def event(
  title: Annotated[str, Form()],
  description: Annotated[str, Form()],
  date: Annotated[str, Form()],
  location: Annotated[str, Form()],
):
  event_id =str(UUID(int=len(events) + 1))
  events.append(Event)

  
  item_data = {
    "id":  event_id,
    "title": title,
    "description": description,
    "date": date,
    "location": location
  }
  
  return {"Message" : "Event created successfully!", "event_data" : item_data}