from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm._orm_constructors import mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    Boolean,
    JSON,
    LargeBinary,
    func,
    Table,
    Column,
    ForeignKey
)

from other.config import config

import other.log.colors as colors
import other.log.logging as logging


log = logging.logging(Name='DB', Color=colors.yellow)

engine = create_async_engine(url=config.POSTGRES_URL)
async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('Users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('Roles.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'Users'

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(1024))
    first_name: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    send_notifications: Mapped[bool] = mapped_column(Boolean(create_constraint=True))
    roles: Mapped[list['Role']] = relationship(
        'Role',
        secondary=user_role,
        back_populates='users',
        lazy='joined'
    )


class Role(Base):
    __tablename__ = 'Roles'

    role_id: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String(256))
    permissions: Mapped[dict] = mapped_column(JSON)
    users: Mapped[list['User']] = relationship(
        'User',
        secondary=user_role,
        back_populates='roles',
        lazy='joined'
    )


class Lesson(Base):
    __tablename__ = 'Lessons'

    lesson_id: Mapped[str] = mapped_column(String(256), primary_key=True)
    homework: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    photo: Mapped[bytes | None] = mapped_column(LargeBinary(8_000_000), nullable=True)
    url: Mapped[str | None] = mapped_column(String(256), nullable=True)


class Schedule(Base):
    __tablename__ = 'Schedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file: Mapped[bytes | None] = mapped_column(LargeBinary(8_000_000), nullable=True)


async def init_db():
    log.init('Connecting to db')
    async with engine.begin() as conn:
        log.init('Creating tables')
        await conn.run_sync(Base.metadata.create_all)
