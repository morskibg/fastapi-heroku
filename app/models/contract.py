from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship


from app.db.base_class import Base

if TYPE_CHECKING:
    from .contractor import Contractor  # noqa: F401
    from .itn_meta import ItnMeta  # noqa: F401


class Contract(Base):
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Numeric(8, 7), index=True)
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    contractor_id = Column(Integer, ForeignKey("contractor.id",
                                               ondelete='CASCADE', onupdate='CASCADE'))

    contractor = relationship(
        "Contractor", back_populates="contracts", lazy='subquery')
    itns = relationship("ItnMeta", back_populates="contract")
