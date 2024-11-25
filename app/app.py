from litestar import Litestar, get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_schema_plugin
from app.models import User


@get(path="/")
async def home() -> str:
    return "Hello"


@get(path="/users")
async def get_users(db_session: AsyncSession) -> list[User]:
    return list(await db_session.scalars(select(User)))


sqlalchemy_plugin = get_schema_plugin()


def create_app() -> Litestar:
    return Litestar(
        route_handlers=[
            home,
            get_users,
        ],
        debug=True,
        plugins=[sqlalchemy_plugin],
    )


app = create_app()
