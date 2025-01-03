from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
@asynccontextmanager
async def life_span(app:FastAPI):
    print(f'server is starting __🛫')
    await init_db()
    yield
    print(f'server has been stopped 🛬__')

version = 'v1'

app = FastAPI(
    title="Bookly",
    description="A REST API for book service",
    version= version,    
    lifespan=life_span
)
app.include_router(book_router, prefix=f'/api/{version}/books',tags=['Books'])