from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        username: str,
        hashed_password: str,
        first_name: str | None = None,
        surname: str | None = None,
        last_name: str | None = None,
    ) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
            first_name=first_name,
            surname=surname,
            last_name=last_name,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
