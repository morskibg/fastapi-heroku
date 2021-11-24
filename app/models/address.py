from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:

    from .itn_meta import ItnMeta  # noqa: F401
    from .contractor import Contractor  # noqa: F401


class Address(Base):
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    postal_code = Column(String, index=True)
    address_line = Column(String, index=True)

    itns = relationship("ItnMeta", back_populates="address")
    contractors = relationship("Contractor", back_populates="address")
