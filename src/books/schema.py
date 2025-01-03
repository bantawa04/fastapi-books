from pydantic import BaseModel
import uuid
from datetime import datetime, date

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language:str
    created_at: datetime
    updated_at: datetime

class CreateBookRequest(BaseModel):
    title: str
    author: str
    publisher: str    
    language:str
    page_count: int
    published_date: str
    
class UpdateBookRequest(BaseModel):    
    title: str
    author: str
    publisher: str  
    page_count: int  
    language:str