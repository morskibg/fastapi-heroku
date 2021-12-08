from typing import Optional
from datetime import date

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime, Numeric
from .contractor import Contractor


# Shared properties
class ContractBase(BaseModel):

    start_date: date
    end_date: date

# Properties to receive on Contract creation


# class ContractCreate(ContractBase):
#     contractor_id: int

class ContractCreate(ContractBase):
    contractor_name: str
    contractor_eik: str
    contractor_city: str
    contractor_postal_code: str
    contractor_address_line: str

    itn: str
    erp: str
    load_type: str
    itn_city: str
    itn_postal_code: str
    itn_address_line: str
    price: float


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
