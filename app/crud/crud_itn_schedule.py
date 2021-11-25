from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.itn_schedule import ItnSchedule

from app.schemas.itn_schedule import ItnScheduleCreate, ItnScheduleUpdate


class CRUDContract(CRUDBase[ItnSchedule, ItnScheduleCreate, ItnScheduleUpdate]):

    def create(
        self, db: Session, *, obj_in: ItnScheduleCreate
    ) -> ItnSchedule:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


itn_schedule = CRUDContract(ItnSchedule)
