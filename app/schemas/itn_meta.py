from .address import Address
from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime, Numeric


# Shared properties
class ItnMetaBase(BaseModel):
    id: str
    erp: str
    load_type: str

    class Config:
        orm_mode = True


# Properties to receive on ItnMeta creation


class ItnMetaCreate(ItnMetaBase):

    address_id: int

    class Config:
        orm_mode = True


# Properties to receive on ItnMeta update
class ItnMetaUpdate(ItnMetaBase):
    pass


# Properties shared by models stored in DB
class ItnMetaInDBBase(ItnMetaBase):

    pass


# Properties to return to client
class ItnMeta(ItnMetaInDBBase):

    address: Address


# Properties properties stored in DB
class ItnMetaInDB(ItnMetaInDBBase):
    pass
