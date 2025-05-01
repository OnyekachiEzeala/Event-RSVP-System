from typing import Annotated, Optional
from datetime import datetime,date
from fastapi import FastAPI, File, UploadFile, Form, status, HTTPException
from pydantic import BaseModel, EmailStr
from uuid import uuid4

app = FastAPI()


class EventBase(BaseModel):
  id: int
  title: str
  description: str
  location: str
  date : date
  # flyer: Optional[Annotated[UploadFile, Form()]]
  # rsvp: list[Annotated[str, Form()]]

class Event(EventBase):
  id: str
  event_create_at: datetime

class RSVP(BaseModel):
  name: str
  email: EmailStr


events: list[EventBase] = []
rsvps: dict[str, list[RSVP]] = {}

# =======Post an Event=======
@app.post("/events" , response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(event : Annotated[Event, Form()]):
  event_dict = event.model_dump()
  event_dict['id']= str(uuid4())
  event_dict['event_create_at'] = datetime.now()
  events.append(event_dict)
  rsvps[event_dict['id']] = []
  return event_dict

# =========Listing the Events======
@app.get("/events", status_code=status.HTTP_200_OK)
async def list_event():
  if not events:
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
  return events


# ========RSVP Processing and Listing========

@app.post("/events/{event_id}/rsvp", status_code=status.HTTP_201_CREATED)
async def rsvp_event(event_id: str, name: str = Form(...), email: str = Form(...)):
  if event_id not in rsvps:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
  rsvp = RSVP(name=name, email=email)
  rsvps[event_id].append(rsvp)
  return {"message": "RSVP successful", "rsvp": rsvp}


