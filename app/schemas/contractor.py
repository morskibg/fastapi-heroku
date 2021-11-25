from typing import Optional

from pydantic import BaseModel

from app.models import address
from .address import Address


# Shared properties
class ContractorBase(BaseModel):
    name: str
    eik: str


# Properties to receive on Contractor creation
class ContractorCreate(ContractorBase):
    address_id: int


# Properties to receive on Contractor update
class ContractorUpdate(ContractorCreate):
    pass


# Properties shared by models stored in DB
class ContractorInDBBase(ContractorBase):
    id: int

    class Config:
        orm_mode = True
        # arbitrary_types_allowed = True


# Properties to return to client
class Contractor(ContractorInDBBase):
    address:  Optional[Address] = None


# Properties properties stored in DB
class ContractorInDB(ContractorInDBBase):
    pass
