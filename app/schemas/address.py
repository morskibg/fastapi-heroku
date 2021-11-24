from typing import Optional

from pydantic import BaseModel


# Shared properties
class AddressBase(BaseModel):
    city: Optional[str] = None
    postal_code: Optional[str] = None
    address_line: str


# Properties to receive on Address creation
class AddressCreate(AddressBase):
    pass


# Properties to receive on Address update
class AddressUpdate(AddressBase):
    pass


# Properties shared by models stored in DB
class AddressInDBBase(AddressBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Address(AddressInDBBase):
    pass


# Properties properties stored in DB
class AddressInDB(AddressInDBBase):
    pass
