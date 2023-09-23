from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.base import Base


class Tracker(Base):
    __tablename__ = "tracker"

    id_ = mapped_column(Integer, primary_key=True)
    longitude: Mapped[str]
    latitude: Mapped[str]
    last_seen: Mapped[datetime]
