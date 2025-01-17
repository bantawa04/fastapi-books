from fastapi import APIRouter, status, Depends
from .schema import CreateUserRequest, User, LoginRequest, UserBooksModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, verify_password
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blacklist
from ..errors import (UserAlreadyExists, InvalidCredentials, InvalidToken)

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin','user'])

REFRESH_TOKEN_EXPIARY = 7


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user_account(
    data: CreateUserRequest, session: AsyncSession = Depends(get_session)
):
    email = data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

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
            user_data = {"email": user.email, "user_uid": str(user.uid), "role": user.role}
            access_token = create_access_token(user_data)

            refresh_token = create_access_token(
                user_data,
                refresh_token=True,
                expiary=timedelta(days=REFRESH_TOKEN_EXPIARY),
            )

            return JSONResponse(
                content={
                    "detail": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {email: user.email, "uid": str(user.uid)},
                }
            )
    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiary_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiary_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]

    await add_jti_to_blacklist(jti)

    return JSONResponse(
        content={"detail": "Logged out sucessfully"}, status_code=status.HTTP_200_OK
    )

@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(user=Depends(get_current_user), _:bool=Depends(role_checker)):
    return user