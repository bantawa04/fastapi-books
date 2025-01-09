from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.schema import CreateReviewRequest
from fastapi.exceptions import HTTPException
from fastapi import status

book_service = BookService()
user_service = UserService()


class ReviewService:

    async def add_review_to_book(self, user_email: str, book_uid: str, review_data: CreateReviewRequest,
                                 session: AsyncSession):
        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)

            if book is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

            user = await user_service.get_user_by_email(user_email, session=session)

            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            new_review = Review(
                **review_data.model_dump()
            )

            new_review.user = user

            new_review.book = book

            session.add(new_review)

            await session.commit()

            return new_review

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")