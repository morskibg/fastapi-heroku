from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .itn_meta import ItnMeta  # noqa: F401


class ItnSchedule(Base):
    itn = Column(String(33), ForeignKey('itn_meta.itn',
                 ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    utc = Column(DateTime, primary_key=True)
    consumption_vol = Column(Numeric(12, 6), nullable=False, default=-1)
    forecast_vol = Column(Numeric(12, 6), nullable=False, default=0)
