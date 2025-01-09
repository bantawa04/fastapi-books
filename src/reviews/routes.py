from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from .schema import CreateReviewRequest
from src.db.main import get_session
from .service import ReviewService
from ..auth.dependencies import get_current_user

review_service = ReviewService()
review_router = APIRouter()


@review_router.post("/books/{book_uid}")
async def create_book(book_uid: str,
                      review_request: CreateReviewRequest,
                      current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)
                      ):
    new_review = await review_service.add_review_to_book(user_email=current_user.email, review_data=review_request,
                                                         book_uid=book_uid, session=session)

    return new_review
