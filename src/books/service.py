from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import CreateBookRequest, UpdateBookRequest
from sqlmodel import select, desc
from .models import Book
from datetime import datetime

class BookService:
    async def get_all_books(self, session: AsyncSession):
        
        statement = select(Book).order_by(desc(Book.created_at))
        
        result = await session.exec(statement)
        
        return result.all()
    
    async def get_book(self,book_uid:str, session: AsyncSession):
        query = select(Book).where(Book.uid == book_uid)
        
        result = await session.exec(query)
        
        return result.first()
    
        return book if book is not None else None
    
    async def create_book(self,book_data:CreateBookRequest, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        
        new_book = Book(
            **book_data_dict
        )
        new_book.published_date = datetime.strptime(book_data_dict['published_date'],"%Y-%m-%d")
        
        session.add(new_book)
        
        await session.commit()
        
        return new_book

    async def update_book(self,book_uid:str,book_data:UpdateBookRequest, session: AsyncSession):
        book_to_update = self.get_book(book_uid, session)
        
        if book_to_update is not None:
        
            update_data_dict = book_data.model_dump()
            
            for key, value in update_data_dict.items():
                setattr(book_data, key, value)
                
            await session.commit()    
            
            return book_to_update
        else:
            return None
            
    
    async def delete_book(self, book_uid:str, session: AsyncSession):
        book = self.get_book(book_uid, session)
        
        if book is not None:
            await session.delete(book)
            await session.commit()
            return {}
        else:
            return None                