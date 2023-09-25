from datetime import datetime
from uuid import UUID

from litestar.contrib.sqlalchemy.base import UUIDBase
from pydantic import BaseModel as _BaseModel
from pydantic import Field
from pydantic_extra_types.coordinate import Latitude, Longitude
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseModel(_BaseModel):
    """Extend Pydantic's BaseModel to enable ORM mode"""

    model_config = {"from_attributes": True}


class Tracker(Base):
    __tablename__ = "tracker"

    id = mapped_column(String, primary_key=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
    last_seen: Mapped[datetime]
    owner_token: Mapped[str]
    shared_token: Mapped[str | None]


class TrackerGet(BaseModel):
    id: str
    longitude: Longitude
    latitude: Latitude
    last_seen: datetime
    owner_token: str
    shared_token: str | None


class TrackerPut(BaseModel):
    id: str | None
    longitude: Longitude | None
    latitude: Latitude | None
    last_seen: datetime | None
    owner_token: str | None
    shared_token: str | None


class TrackerPost(BaseModel):
    id: str
    longitude: Longitude = Field(default=51.9522542)
    latitude: Latitude = Field(default=7.6378045)
    last_seen: datetime
    owner_token: str
    shared_token: str | None


class Owner(Base):
    __tablename__ = "owner"

    id = mapped_column(String, primary_key=True)
    longitude: Mapped[str]
    latitude: Mapped[str]
    last_seen: Mapped[datetime]
