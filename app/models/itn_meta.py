from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.db.base_class import Base


if TYPE_CHECKING:
    from .address import Address  # noqa: F401
    from .contract import Contract  # noqa: F401


class ItnMeta(Base):
    __tablename__ = "itn_meta"
    id = Column(String, primary_key=True, index=True, unique=True)
    erp = Column(String, index=True)
    load_type = Column(String, index=True)
    address_id = Column(Integer, ForeignKey(
        "address.id", ondelete='CASCADE', onupdate='CASCADE'))
    address = relationship("Address", back_populates="itns", lazy='subquery')



# event.listen(ItnMeta, 'after_update', ItnSchedule.update)
