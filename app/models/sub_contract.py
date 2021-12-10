from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import event
from .itn_schedule import ItnSchedule


from app.db.base_class import Base

if TYPE_CHECKING:
    from .contract import Contract  # noqa: F401
    from .itn_schedule import ItnSchedule  # noqa: F401


class SubContract(Base):
    __tablename__ = "sub_contract"
    itn = Column(String(33), ForeignKey('itn_meta.id',
                 ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    price = Column(Numeric(8, 7), index=True)
    start_date = Column(DateTime, index=True, primary_key=True)
    end_date = Column(DateTime, index=True, primary_key=True)
    contract_id = Column(Integer, ForeignKey("contract.id",
                                             ondelete='CASCADE', onupdate='CASCADE'))

    # contract = relationship(
    #     "Contract", backref="sub_contracts")
    contract = relationship(
        "Contract", back_populates="sub_contracts", lazy='subquery')

    # meta = relationship("ItnMeta", back_populates="contract")


event.listen(SubContract, 'after_insert', ItnSchedule.autoinsert_new)
event.listen(SubContract, 'after_delete', ItnSchedule.on_delete_contract)
