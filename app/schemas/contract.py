from typing import Optional
from datetime import date

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime, Numeric
from .contractor import Contractor


# Shared properties
class ContractBase(BaseModel):
    price: float
    start_date: date
    end_date: date

# Properties to receive on Contract creation


class ContractCreate(ContractBase):
    contractor_id: int


# Properties to receive on Contract update
class ContractUpdate(ContractBase):
    pass


# Properties shared by models stored in DB
class ContractInDBBase(ContractBase):
    id: int

    class Config:
        orm_mode = True
        # arbitrary_types_allowed = True


# Properties to return to client
class Contract(ContractInDBBase):
    contractor: Contractor  # Optional[Contractor] = None


# Properties properties stored in DB
class ContractInDB(ContractInDBBase):
    pass
