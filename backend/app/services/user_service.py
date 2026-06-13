from app.core.db_manager import DBManager
from app.core.exceptions import (
    UserAlreadyExistsError,
)
from app.core.security import security


class UserService:
    def __init__(self, db: DBManager):
        self.db = db

    async def register(self, name: str, password: str):
        existing = await self.db.users.get_user_by_name(name)

        if existing:
            raise UserAlreadyExistsError('User already exists')

        user = await self.db.users.create_user(
            name=name,
            password_hash=security.hash_password(password),
        )
        await self.db.flush()

        return user
