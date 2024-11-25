import asyncio
from typing import AsyncGenerator, AsyncIterator

import pytest
from httpx import AsyncClient, ASGITransport
from litestar import Litestar
from polyfactory import BaseFactory
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.app import sqlalchemy_plugin, create_app
from app.db import engine, Base


@pytest.fixture
def f_session_maker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture
async def f_session(f_session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with f_session_maker() as session:
        yield session


@pytest.fixture
def f_app() -> Litestar:
    return create_app()


@pytest.fixture
async def f_client(f_app: Litestar) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=f_app),
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True)
async def _patch_db(
    f_app: "Litestar",
    f_session_maker: async_sessionmaker[AsyncSession],
    f_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sqlalchemy_config = sqlalchemy_plugin._config
    if isinstance(sqlalchemy_config, list):
        sqlalchemy_config = sqlalchemy_config[0]
    monkeypatch.setitem(
        f_app.state,
        sqlalchemy_config.session_maker_app_state_key,
        f_session_maker,
    )
    BaseFactory.__async_session__ = f_session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
