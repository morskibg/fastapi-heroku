from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.itn_meta import ItnMeta

from app.schemas.itn_meta import ItnMetaCreate, ItnMetaUpdate


class CRUDContract(CRUDBase[ItnMeta, ItnMetaCreate, ItnMetaUpdate]):

    def create(
        self, db: Session, *, obj_in: ItnMetaCreate
    ) -> ItnMeta:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


itn_meta = CRUDContract(ItnMeta)
