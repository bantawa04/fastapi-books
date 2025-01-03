
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schema import Book, CreateBookRequest, UpdateBookRequest
from typing import List
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService

book_router = APIRouter()
book_service = BookService()

@book_router.get('/', response_model=List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session))->list:
    books = await book_service.get_all_books(session)
    return books

@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)    
async def create_book(book_data:CreateBookRequest,session:AsyncSession = Depends(get_session))->dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book
    
@book_router.get('/{book_uid}')
async def get_book(book_uid: int,session:AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)
    
    if book:
        return  book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')


@book_router.patch('/{book_uid}')
async def update_book(book_uid:int, book_update: UpdateBookRequest, session:AsyncSession = Depends(get_session))->dict:
    update_book = await book_service.update_book(book_uid, book_update, session)
    
    if update_book:
        return update_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')            

@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)    
async def delete_book(book_uid:int, session:AsyncSession = Depends(get_session)):
    
    book_to_delete = await book_service.delete_book(book_uid, session)
    
    if book_to_delete:
        return None
    else:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")            