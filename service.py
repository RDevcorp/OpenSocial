from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import *
from models import *

class UsersRepository:
    async def get_user_by_email(session: AsyncSession, user_email: str) -> UserBaseSchema:
        result = await session.execute(select(User).where(User.c.emai == user_email))
        return result.all()


