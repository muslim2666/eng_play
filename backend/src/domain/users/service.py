from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.models import User
from src.domain.users.repository import UserRepository
from src.domain.users.schemas import Token, UserCreate, UserLogin
from src.domain.users.security import (
    create_access_token,
    hash_password,
    verify_password,
)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(session)

    async def register(self, data: UserCreate) -> User:
        existing = await self.repo.get_by_username(data.username)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken",
            )

        return await self.repo.create(
            username=data.username,
            hashed_password=hash_password(data.password),
            first_name=data.first_name,
            surname=data.surname,
            last_name=data.last_name,
        )

    async def login(self, data: UserLogin) -> Token:
        user = await self.repo.get_by_username(data.username)
        if user is None or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return Token(access_token=create_access_token(str(user.id)))

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.repo.get_by_id(user_id)
