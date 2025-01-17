from src.db.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schema import CreateUserRequest
from .utils import generate_password_hash


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        query = select(User).where(User.email == email)

        result = await session.exec(query)

        return result.first()

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_user(self, user_data: CreateUserRequest, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password = generate_password_hash(user_data_dict["password"])
        new_user.role = "user"

        session.add(new_user)

        await session.commit()

        return new_user
