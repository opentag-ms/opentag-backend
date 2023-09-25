from typing import Annotated

from litestar import delete, get, post, put
from litestar.controller import Controller
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from sqlalchemy import sql
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from model.models import Tracker, TrackerPost, TrackerPut


async def get_tracker_async(tracker_id: str, session: AsyncSession) -> Tracker:
    query = sql.select(Tracker).where(Tracker.id == tracker_id)
    result = await session.execute(query)
    try:
        return result.scalar_one()
    except NoResultFound as e:
        raise NotFoundException(detail=f"Tracker {tracker_id!r} not found") from e


async def update_tracker_async(tracker_id: str, data: TrackerPut, session: AsyncSession) -> Tracker:
    try:
        await session.merge(data)
        return await get_tracker_async(tracker_id=tracker_id, session=session)
    except NoResultFound as e:
        raise NotFoundException(detail=f"Tracker {tracker_id!r} not found") from e


class TrackerController(Controller):
    path = "/devices"
    token_header_name = "Authorization"

    @get("/")
    async def get_trackers(self, transaction: AsyncSession) -> list[Tracker]:
        query = sql.select(Tracker)
        result = await transaction.execute(query)
        return list(result.scalars().all())

    @get("/{tracker_id:str}")
    async def get_tracker(self, tracker_id: str, transaction: AsyncSession) -> Tracker:
        return await get_tracker_async(tracker_id, transaction)

    @post("/")
    async def create_tracker(self, data: Tracker, transaction: AsyncSession) -> Tracker:
        transaction.add(data)
        return data

    @put("/{tracker_id:str}")
    async def update_tracker(self, tracker_id: str, data: Tracker, transaction: AsyncSession) -> Tracker:
        tracker = await update_tracker_async(tracker_id, data, transaction)
        return tracker

    @delete("/{tracker_id:str}")
    async def delete_tracker(self, tracker_id: str, transaction: AsyncSession) -> None:
        query = sql.delete(Tracker).where(Tracker.id == tracker_id)
        await transaction.execute(query)

    @get("/{tracker_id:str}/start_sharing")
    async def tracker_share_start(
        self, tracker_id: str, token: Annotated[str, Parameter(header=token_header_name)], transaction: AsyncSession
    ) -> str:
        pass

    @get("/{tracker_id:str}/stop_sharing")
    async def tracker_share_stop(
        self, tracker_id: str, token: Annotated[str, Parameter(header=token_header_name)], transaction: AsyncSession
    ) -> None:
        pass
