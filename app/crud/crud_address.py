from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate, ]):

    def create(
        self, db: Session, *, obj_in: AddressCreate
    ) -> Address:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def filter_by_all(
        self, db: Session, *, city: str, postal_code: str, address_line: str
    ) -> Address:
        db_obj = (
            db.query(Address)
            .filter(Address.city == city, Address.postal_code == postal_code, Address.address_line == address_line)
            .first())

        return db_obj

    def is_match(
        self, db: Session, *, obj_in: AddressCreate, address_id: int
    ) -> bool:
        return (obj_in.id == address_id)


address = CRUDAddress(Address)
