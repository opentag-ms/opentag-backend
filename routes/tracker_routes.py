from typing import Any
from collections.abc import AsyncGenerator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from litestar import Litestar, get, post, put
from model.tracker import Tracker

async def get_tracker(tracker_id: Any, session: AsyncSession) -> Tracker:
    query = select(Tracker).where(Tracker.id == tracker_id)
    result = await session.execute(query)
    try:
        return result.scalar_one()
    except NoResultFound as e:
        raise NotFoundException(detail=f"Tracker {tracker_id!r} not found") from e


async def get_trackers(transaction: AsyncSession, done: bool | None = None) -> list[Tracker]:
    return await get_trackers(done, transaction)


@put("/{tracker_id:int}")
async def update_tracker(tracker_id: int, data: Tracker, transaction: AsyncSession) -> Tracker:
    tracker = await get_tracker(tracker_id, transaction)
    tracker.name = data.name
    tracker.fullname  = data.fullname
    tracker.nickname = data.nickname
    return tracker


@post("/")
async def add_tracker(data: Tracker, transaction: AsyncSession) -> Tracker:
    transaction.add(data)
    return data

