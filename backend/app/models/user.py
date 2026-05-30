from datetime import datetime
from uuid import uuid4


from sqlalchemy import DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

    cart_items: Mapped['Cart'] = relationship(back_populates='user')
    sessions: Mapped[list['UserSession']] = relationship(back_populates='user', cascade='all, delete-orphan')


class UserSession(Base):
    __tablename__ = 'sessions'

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True)

    expires_at: Mapped[datetime] = mapped_column(DateTime(), index=True)
    last_refreshed_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates='sessions')
