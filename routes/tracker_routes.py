from typing import Any
from collections.abc import AsyncGenerator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from litestar import Litestar, get, post, put
from litestar.controller import Controller
from model.tracker import Tracker

async def get_tracker_async(tracker_id: int, session: AsyncSession) -> Tracker:
    query = select(Tracker).where(Tracker.id == tracker_id)
    result = await session.execute(query)
    try:
        return result.scalar_one()
    except NoResultFound as e:
        raise NotFoundException(detail=f"Tracker {tracker_id!r} not found") from e


async def get_trackers(transaction: AsyncSession, done: bool | None = None) -> list[Tracker]:
    pass


class TrackerController(Controller):
	path = "/tracker"

	@get("/{tracker_id:int}")
	async def get_tracker(self, tracker_id: int, transaction: AsyncSession) -> Tracker:
	    tracker = await get_tracker_async(tracker_id, transaction)
	    return tracker


	@put("/{tracker_id:int}")
	async def update_tracker(self, tracker_id: int, data: Tracker, transaction: AsyncSession) -> Tracker:
	    tracker = await get_tracker_async(tracker_id, transaction)
	    tracker.name = data.name
	    tracker.fullname  = data.fullname
	    tracker.nickname = data.nickname
	    return tracker


	@post("/")
	async def add_tracker(self, data: Tracker, transaction: AsyncSession) -> Tracker:
	    transaction.add(data)
	    return data

