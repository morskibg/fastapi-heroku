from typing import Optional
from datetime import date

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime, Numeric

# from app.models.contract import Contract
# from .contract import Contract


# Shared properties
class SubContractBase(BaseModel):
    itn: str
    start_date: date
    end_date: date
    price: float

    class Config:
        orm_mode = True

# Properties to receive on Contract creation


# class ContractCreate(SubContractBase):
#     contractor_id: int

class SubContractCreate(SubContractBase):
    contract_id: int

    # itn: str
    # erp: str
    # load_type: str
    # itn_city: str
    # itn_postal_code: str
    # itn_address_line: str


# Properties to receive on Contract update
class SubContractUpdate(SubContractBase):
    pass


# Properties shared by models stored in DB
class SubContractInDBBase(SubContractBase):
    pass
    # id: int

    # class Config:
    #     orm_mode = True
    # arbitrary_types_allowed = True


# Properties to return to client
class SubContract(SubContractInDBBase):
    pass
    # contract: Optional[Contract] = None
    # contract: Contract  # Optional[Contractor] = None

    # Properties properties stored in DB


class SubContractInDB(SubContractInDBBase):
    pass
