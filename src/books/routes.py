from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schema import Book, CreateBookRequest, UpdateBookRequest
from typing import List
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer

book_router = APIRouter()
book_service = BookService()
authorization = AccessTokenBearer()


@book_router.get("/", response_model=List[Book])
async def get_all_books(
    session: AsyncSession = Depends(get_session), security=Depends(authorization)
) -> list:
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(
    book_data: CreateBookRequest,
    session: AsyncSession = Depends(get_session),
    security=Depends(authorization),
) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_uid}", response_model=Book)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
     security=Depends(authorization)
) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(
    book_uid: str,
    book_update: UpdateBookRequest,
    session: AsyncSession = Depends(get_session),
    security=Depends(authorization),
) -> dict:
    update_book = await book_service.update_book(book_uid, book_update, session)

    if update_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:
        return update_book


@book_router.delete("/{book_uid}")
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    security=Depends(authorization),
):

    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete:
        return {"detail": "Book deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
