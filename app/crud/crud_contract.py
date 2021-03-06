from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.contract import Contract
from app.models.sub_contract import SubContract

from app.schemas.contract import ContractCreate, ContractUpdate


class CRUDContract(CRUDBase[Contract, ContractCreate, ContractUpdate]):

    def create(
        self, db: Session, *, obj_in: ContractCreate
    ) -> Contract:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        print(f'in create conteract crud --> {db_obj}')
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def get_full_data(self, db: Session, *, obj_in: ContractCreate
    #                   ) -> Contract:


contract = CRUDContract(Contract)
