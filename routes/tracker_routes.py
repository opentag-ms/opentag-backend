from collections.abc import AsyncGenerator
from typing import Any

from litestar import Litestar, get, post, put
from litestar.controller import Controller
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from model.tracker import Tracker


async def get_tracker_async(tracker_id: int, session: AsyncSession) -> Tracker:
    query = select(Tracker).where(Tracker.id == tracker_id)
    result = await session.execute(query)
    try:
        return result.scalar_one()
    except NoResultFound as e:
        raise NotFoundException(detail=f"Tracker {tracker_id!r} not found") from e


async def update_tracker_async(data: Tracker, session: AsyncSession) -> Tracker:
    result = await session.merge(data)
    try:
        return result
    except NoResultFound as e:
        raise NotFoundException(detail=f"Tracker {tracker_id!r} not found") from e


class TrackerController(Controller):
    path = "/devices"

    @get("/{tracker_id:int}")
    async def get_tracker(self, tracker_id: int, transaction: AsyncSession) -> Tracker:
        tracker = await get_tracker_async(tracker_id, transaction)
        return tracker

    @put("/")
    async def update_tracker(self, data: Tracker, transaction: AsyncSession) -> Tracker:
        tracker = await update_tracker_async(data, transaction)
        return tracker
