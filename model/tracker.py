import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Integer, String, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from model.base import Base


class Tracker(Base):
    __tablename__ = "tracker"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]] = mapped_column(String(64))
    # create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
