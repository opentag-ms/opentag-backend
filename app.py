from typing import Any
from collections.abc import AsyncGenerator
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from litestar import Litestar, get
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
import uvicorn

from routes import tracker_routes

import model.base

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
    [tracker_routes.TrackerController,],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
    debug=True
)


def create_table_if_not_exists():
    engine = create_engine('sqlite:///opentag.sqlite', echo = True)
    meta = model.base.Base.metadata
    meta.create_all(engine)


if __name__ == "__main__":
    create_table_if_not_exists()
    uvicorn.run("app:app")



