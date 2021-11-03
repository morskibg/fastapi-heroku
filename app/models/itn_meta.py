from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .address import Address  # noqa: F401
    from .contract import Contract  # noqa: F401


class ItnMeta(Base):
    __tablename__ = "itn_meta"
    itn = Column(String, primary_key=True, index=True)
    erp = Column(String, index=True)
    contract_id = Column(Integer, ForeignKey(
        "contract.id", ondelete='CASCADE', onupdate='CASCADE'))
    address_id = Column(Integer, ForeignKey(
        "address.id", ondelete='CASCADE', onupdate='CASCADE'))
    contract = relationship("Contract", back_populates="itns")
    address = relationship("Address", back_populates="itns")
