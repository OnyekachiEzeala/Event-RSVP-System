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
    print(f"Received flyer: {flyer.filename if flyer else 'No file uploaded'}")
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
