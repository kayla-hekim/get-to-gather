from app.models.User import User
from typing import Dict
from app.models.user_db import UserDB
from sqlalchemy.future import select


async def get_or_create_user(db, user_id):
    result = await db.execute(select(UserDB).where(UserDB.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        user = UserDB(user_id=user_id)
        db.add(user)
        await db.commit()
    return user