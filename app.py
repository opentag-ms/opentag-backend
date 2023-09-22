from collections.abc import AsyncGenerator
from typing import Any

import uvicorn
from litestar import Litestar, get
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import model.base
from routes import tracker_routes


async def provide_transaction(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    try:
        async with db_session.begin():
            yield db_session
    except IntegrityError as exc:
        raise ClientException(
            status_code=HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


db_config = SQLAlchemyAsyncConfig(connection_string="sqlite+aiosqlite:///opentag.sqlite")

app = Litestar(
    [
        tracker_routes.TrackerController,
    ],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
    debug=True,
)


def create_table_if_not_exists():
    engine = create_engine("sqlite:///opentag.sqlite", echo=True)
    meta = model.base.Base.metadata
    meta.create_all(engine)


if __name__ == "__main__":
    create_table_if_not_exists()
    uvicorn.run("app:app")
