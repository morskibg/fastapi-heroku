from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.contractor import Contractor
from app.models.address import Address
from app.schemas.contractor import ContractorCreate, ContractorUpdate


class CRUDContractor(CRUDBase[Contractor, ContractorCreate, ContractorUpdate]):

    def create(
        self, db: Session, *, obj_in: ContractorCreate
    ) -> Contractor:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Contractor]:
        return (db.query(Contractor).outerjoin(Address, Address.id == Contractor.address_id).offset(skip).limit(limit).all())

    def filter_by_eik(
        self, db: Session, *,  eik: str
    ) -> Contractor:
        print("🚀 ~ file: crud_contractor.py ~ line 31 ~ eik", eik)
        # db.query(Contractor).filter(Contractor.eik == '12345').first()
        db_obj = (
            db.query(Contractor)
            .filter(Contractor.eik == eik)
            .first())
        print("🚀 ~ file: crud_contractor.py ~ line 36 ~ db_obj", db_obj)

        return db_obj

    def is_match(
        self, db: Session, *, obj_in: ContractorCreate, name: str, eik: str
    ) -> bool:
        return (obj_in.name == name) & (obj_in.eik == eik)


contractor = CRUDContractor(Contractor)
