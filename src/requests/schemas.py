import datetime
from pydantic import BaseModel

from .models import Status


class RequestSchema(BaseModel):
    id: int
    needy_id: int
    volunteer_id: int
    location: str
    description: str
    status: Status
    data_created: datetime.date
    time_created: datetime.time 
    data_completed: datetime.date 
    time_completed: datetime.time


class AddRequestSchema(BaseModel):
    location: str 
    description: str
   
    
    