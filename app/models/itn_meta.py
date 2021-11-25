from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import event

from app.db.base_class import Base
from .itn_schedule import ItnSchedule

if TYPE_CHECKING:
    from .address import Address  # noqa: F401
    from .contract import Contract  # noqa: F401


class ItnMeta(Base):
    __tablename__ = "itn_meta"
    id = Column(String, primary_key=True, index=True, unique=True)
    erp = Column(String, index=True)
    contract_id = Column(Integer, ForeignKey(
        "contract.id", ondelete='CASCADE', onupdate='CASCADE'))
    address_id = Column(Integer, ForeignKey(
        "address.id", ondelete='CASCADE', onupdate='CASCADE'))
    contract = relationship("Contract", back_populates="itns", lazy='subquery')
    address = relationship("Address", back_populates="itns", lazy='subquery')


event.listen(ItnMeta, 'after_insert', ItnSchedule.autoinsert_new)
# a = 99
