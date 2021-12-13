from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.sub_contract import SubContract

from app.schemas.sub_contract import SubContractCreate, SubContractUpdate


class CRUDSubContract(CRUDBase[SubContract, SubContractCreate, SubContractUpdate]):

    def create(
        self, db: Session, *, obj_in: SubContractCreate
    ) -> SubContract:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        print(f'in create SUBCONTRACT crud --> {db_obj}')
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_contract_id(
        self, db: Session, *, contract_id: int
    ) -> SubContract:
        db_obj = (db.query(SubContract)
                  .filter(SubContract.contract_id == contract_id)
                  .first())
        return db_obj


sub_contract = CRUDSubContract(SubContract)
