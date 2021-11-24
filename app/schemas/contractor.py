from typing import Optional

from pydantic import BaseModel
from ..models import Address


# Shared properties
class ContractorBase(BaseModel):
    name: str
    eik: str


# Properties to receive on Contractor creation
class ContractorCreate(ContractorBase):
    pass


# Properties to receive on Contractor update
class ContractorUpdate(ContractorBase):
    pass


# Properties shared by models stored in DB
class ContractorInDBBase(ContractorBase):
    id: int
    address: Address

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# Properties to return to client
class Contractor(ContractorInDBBase):

    pass


# Properties properties stored in DB
class ContractorInDB(ContractorInDBBase):
    pass
