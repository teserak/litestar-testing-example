from litestar.plugins.sqlalchemy import (
    SQLAlchemyAsyncConfig,
    AsyncSessionConfig,
    SQLAlchemyPlugin,
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


engine = create_async_engine(
    url="sqlite+aiosqlite:///:memory:",
    echo=True,
)


def get_schema_plugin():
    sqlalchemy_config = SQLAlchemyAsyncConfig(
        create_all=True,
        before_send_handler="autocommit",
        session_config=AsyncSessionConfig(expire_on_commit=False),
        metadata=Base.metadata,
        engine_instance=engine,
    )
    return SQLAlchemyPlugin(config=sqlalchemy_config)
