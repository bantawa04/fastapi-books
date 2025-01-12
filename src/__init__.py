from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.dependencies import RoleChecker
from src.tags.routes import tags_router

role_checker = RoleChecker(["admin", "user"])
from .errors import (
    create_exception_handler,
    InvalidCredentials,
    TagAlreadyExists,
    TagNotFound,
    UserNotFound,
    UserAlreadyExists,
    BookNotFound,
    InsufficientPermission,
    InvalidToken,
    AccessTokenRequired,
    RefreshTokenRequired,
    RevokedToken
)


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

app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "User not found",
            "error_code": "user_not_found",
        },
    ),
)
app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Book not found",
            "error_code": "book_not_found",
        },
    ),
)
app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        initial_detail={
            "message": "Invalid Email Or Password",
            "error_code": "invalid_email_or_password",
        },
    ),
)
app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token is invalid Or expired",
            "resolution": "Please get new token",
            "error_code": "invalid_token",
        },
    ),
)
app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token is invalid or has been revoked",
            "resolution": "Please get new token",
            "error_code": "token_revoked",
        },
    ),
)
app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Please provide a valid access token",
            "resolution": "Please get an access token",
            "error_code": "access_token_required",
        },
    ),
)
app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Please provide a valid refresh token",
            "resolution": "Please get an refresh token",
            "error_code": "refresh_token_required",
        },
    ),
)
app.add_exception_handler(
    InsufficientPermission,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "You do not have enough permissions to perform this action",
            "error_code": "insufficient_permissions",
        },
    ),
)
app.add_exception_handler(
    TagNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={"message": "Tag Not Found", "error_code": "tag_not_found"},
    ),
)

app.add_exception_handler(
    TagAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Tag Already exists",
            "error_code": "tag_exists",
        },
    ),
)

app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Book Not Found",
            "error_code": "book_not_found",
        },
    ),
)


@app.exception_handler(500)
async def internal_server_error(request, exc):
    return JSONResponse(
        content={
            "message": "Oops! Something went wrong",
            "error_code": "server_error",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


app.include_router(
    book_router,
    prefix=f"/api/{version}/books",
    tags=["Books"],
    dependencies=[Depends(role_checker)],
)
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Review"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["Tag"])
