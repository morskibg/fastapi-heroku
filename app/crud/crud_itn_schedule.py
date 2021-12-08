from typing import List
from datetime import datetime

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

    def get_schedule_by_itn_for_period_utc(
        self, db: Session, *, itn: str, start_date: datetime, end_date: datetime
    ) -> List[ItnSchedule]:
        db_obj = (db.query(ItnSchedule)
                  .filter(ItnSchedule.utc >= start_date, ItnSchedule.utc <= end_date, ItnSchedule.itn == itn)
                  .all())
        return db_obj

    def get_unique_itn_schedule_for_period_utc(
        self, db: Session, *, start_date: datetime, end_date: datetime
    ) -> List[ItnSchedule]:
        db_obj = (db.query(ItnSchedule)
                  .filter(ItnSchedule.utc >= start_date, ItnSchedule.utc <= end_date)
                  .distinct(ItnSchedule.itn)
                  .all())

        return db_obj

    def get_schedule_by_id(
        self, db: Session, *, itn: str
    ) -> List[ItnSchedule]:
        db_obj = (db.query(ItnSchedule)
                  .filter(ItnSchedule.itn == itn)
                  .all())
        # print(f'SSSSSSSSSSSSss ---> {db_obj[0].itn}')
        return db_obj


itn_schedule = CRUDContract(ItnSchedule)
