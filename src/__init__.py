from fastapi import Depends, FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.dependencies import RoleChecker

role_checker = RoleChecker(["admin", "user"])


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"server is starting __🛫")
    await init_db()
    yield
    print(f"server has been stopped 🛬__")


version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for book service",
    version=version,
)
app.include_router(
    book_router,
    prefix=f"/api/{version}/books",
    tags=["Books"],
    dependencies=[Depends(role_checker)],
)
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
