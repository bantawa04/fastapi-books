from fastapi import APIRouter, status, Depends
from .schema import CreateUserRequest, User, LoginRequest
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_token, verify_password
from fastapi.responses import JSONResponse
from datetime import timedelta


auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIARY= 7

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user_account(
    data: CreateUserRequest, session: AsyncSession = Depends(get_session)
):
    email = data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(data, session)

    return new_user


@auth_router.post("/login")
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    email = data.email
    password = data.password

    user = await user_service.get_user_by_email(email, session)
    
    if user is not None:
        password_valid = verify_password(password, user.password)

        if password_valid:
            user_data = {"email": user.email, "user_uid": str(user.uid)}
            access_token = create_access_token(
                user_data
            )

            refresh_token = create_access_token(
                user_data,
                refresh_token=True,
                expiary=timedelta(days=REFRESH_TOKEN_EXPIARY)
            )
           
            return JSONResponse(
                content={
                    "detail": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        email: user.email,
                        "uid": str(user.uid)
                    }
                }
            ) 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid email or password")           