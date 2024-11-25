from typing import TypeVar, Generic

from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import engine
from app.models import User

T = TypeVar("T")


class BaseFactory(Generic[T], SQLAlchemyFactory[T]):
    __async_session__ = AsyncSession(engine)
    __is_base_factory__ = True


class UserFactory(BaseFactory[User]):
    __model__ = User
