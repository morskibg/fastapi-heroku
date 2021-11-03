from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .contract import Contract  # noqa: F401


class Contractor(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    eik = Column(String, index=True)

    contracts = relationship("Contract", back_populates="contractor")
