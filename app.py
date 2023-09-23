from collections.abc import AsyncGenerator

import uvicorn
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from model.base import Base
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


async def create_tables_if_not_exist() -> None:
    """Initializes the database."""
    async with db_config.create_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = Litestar(
    route_handlers=[tracker_routes.TrackerController],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
    on_startup=[create_tables_if_not_exist],
    debug=True,
)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
