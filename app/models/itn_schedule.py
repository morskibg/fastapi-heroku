from typing import TYPE_CHECKING

import pandas as pd
from sqlalchemy import Column, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models import contractor
from app.models.contract import Contract
from app.core.utils import *
from app.db.session import SessionLocal

if TYPE_CHECKING:
    from .itn_meta import ItnMeta  # noqa: F401


class ItnSchedule(Base):
    __tablename__ = "itn_schedule"
    itn = Column(String(33), ForeignKey('itn_meta.id',
                 ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    utc = Column(DateTime, primary_key=True)
    consumption_vol = Column(Numeric(12, 6), nullable=False, default=-1)
    forecast_vol = Column(Numeric(12, 6), nullable=False, default=0)

    meta = relationship("ItnMeta")

    @classmethod
    def autoinsert_new(cls, mapper, connection, target):
        db = SessionLocal()
        print(f'in autoinsert_new')
        meta = target
        table_name = ItnSchedule.__table__
        start_date, end_date = db.query(
            Contract.start_date, Contract.end_date).filter(Contract.id == meta.contract_id).all()[0]
        end_date = end_date.replace(hour=23, minute=0, second=0, microsecond=0)

        start_date_utc = convert_date_to_utc_with_hours(
            'Europe/Sofia', start_date)
        end_date_utc = convert_date_to_utc_with_hours(
            'Europe/Sofia', end_date)

        time_series = pd.date_range(
            start=start_date_utc, end=end_date_utc, freq='h')

        delete_query = table_name.delete().where((ItnSchedule.itn == meta.id) & (
            ItnSchedule.utc >= start_date_utc) & (ItnSchedule.utc <= end_date_utc))
        connection.execute(delete_query)
        schedule_df = pd.DataFrame(time_series, columns=['utc'])

        schedule_df['itn'] = target.id
        schedule_df['consumption_vol'] = -1
        schedule_df['forecast_vol'] = -1
        schedule_df.to_sql(str(table_name),
                           con=connection, if_exists='append', index=False)
