from pydantic import BaseModel, Field
import uuid
from datetime import datetime, date
from typing import Optional

class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=5)
    review_text: str
    book_uid: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

class CreateReviewRequest(BaseModel):
    rating: int = Field(lt=5)
    review_text: str