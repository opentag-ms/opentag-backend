from typing import Any
from collections.abc import AsyncGenerator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from litestar import Litestar, get
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
import uvicorn

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
    [tracker_routes.update_tracker, tracker_routes.add_tracker],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
    debug=True
)


if __name__ == "__main__":
    uvicorn.run("app:app")

