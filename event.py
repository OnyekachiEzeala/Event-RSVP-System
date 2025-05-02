from typing import Annotated, Optional
from datetime import datetime,date
from fastapi import FastAPI, File, UploadFile, Form, status, HTTPException, Depends
from pydantic import BaseModel
from uuid import UUID

app = FastAPI()


class EventBase(BaseModel):
  title: str
  description: str
  location: str
  date : date
  flyer: Optional[UploadFile] = None
  rsvp: list [str] = []

class Event(EventBase):
  pass

class RSVP(BaseModel):
  name: str
  email: str


events: list[EventBase] = []
# rsvps: dict[str, list[RSVP]] = {}

# store_email = []

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

# ========Get Events by ID========
@app.get ("/events/{event_id}", status_code = status.HTTP_200_OK)
def get_event_by_id(event_id:int):
    for event in events:
        if event["id"] == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")



# def check_if_user_exists(email: str):
#     for event in events:
#         if event.email == email:
#             return True
#     return False

@app.post("/events/{event_id}/rsvp", status_code=status.HTTP_201_CREATED)
async def rsvp_event(event_id:int, response: Annotated[RSVP, Form()]):
  
  # if not check_if_user_exists(response.email):
  #   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
  # 1. Find the event
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
  # 3. If not found, return 404
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")


@app.get("/events/{event_id}/rsvps", status_code=status.HTTP_200_OK)
def list_rsvps(event_id:int):
   for event in events:
      if event["id"] == event_id:
         return event.get("rsvp", [])
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Event not found')
