from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import Contact
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date

from app.crud.base import CRUDBase
from app.models.itn_meta import ItnMeta
from app.models.contract import Contract

from app.schemas.itn_meta import ItnMetaCreate, ItnMetaUpdate


class CRUDItnMeta(CRUDBase[ItnMeta, ItnMetaCreate, ItnMetaUpdate]):

    def create(
        self, db: Session, *, obj_in: ItnMetaCreate
    ) -> ItnMeta:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_id(
        self, db: Session, *, id: str
    ) -> ItnMeta:
        print('in get_by_id', id)
        db_obj = db.query(ItnMeta).filter(ItnMeta.id == id).first()
        return db_obj

    def get(
        self, db: Session, *, id: str, contract_id: int
    ) -> ItnMeta:
        db_obj = db.query(ItnMeta).filter(ItnMeta.id == id,
                                          ItnMeta.contract_id == contract_id).first()
        print("🚀 ~ file: crud_itn_meta.py ~ line 39 ~ db_obj", db_obj)
        return db_obj

    def get_all_availabe_for_period(
        self, db: Session, *, start_date: date, end_date: date
    ) -> list[ItnMeta]:
        db_obj = (db.query(ItnMeta)
                  .join(Contract, Contract.id == ItnMeta.contract_id)
                  .filter(or_(Contract.start_date > end_date, Contract.end_date < start_date))
                  .all())
        print(db_obj)
        return db_obj

    def is_match(
        self, db: Session, *, obj_in: ItnMetaCreate, erp: str, load_type: str
    ) -> bool:
        return (obj_in.erp == erp) & (obj_in.load_type == load_type)

    # def filter_by_all(
    #     self, db: Session, *, erp: str, postal_code: str, address_line: str
    # ) -> ItnMeta:
    #     db_obj = (
    #         db.query(ItnMeta)
    #         .filter(Address.city == city, Address.postal_code == postal_code, Address.address_line == address_line)
    #         .first())

    #     return db_obj


itn_meta = CRUDItnMeta(ItnMeta)
