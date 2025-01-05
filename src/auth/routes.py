from fastapi import APIRouter, status, Depends
from .schema import CreateUserRequest, User
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model= User)
async def create_user_account(
    data: CreateUserRequest,session:AsyncSession = Depends(get_session)
):
    email = data.email

    user_exists = await user_service.user_exists(email,session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(data,session)

    return new_user
