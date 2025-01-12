from typing import Optional

from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=5)
    review_text: str
    book_uid: Optional[uuid.UUID]
    user_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

class BookResponse(BaseModel):
    uid: uuid.UUID
    rating: int
    review_text: str
    book_uid: Optional[uuid.UUID]
    user_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # This enables ORM mode

class CreateReviewRequest(BaseModel):
    rating: int = Field(lt=5)
    review_text: str
