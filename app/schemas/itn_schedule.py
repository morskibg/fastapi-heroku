from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime, Numeric

from .itn_meta import ItnMeta


# Shared properties
class ItnScheduleBase(BaseModel):
    itn: str
    utc: datetime
    consumption_vol: float
    forecast_vol: float

    class Config:
        orm_mode = True


# Properties to receive on ItnSchedule creation


class ItnScheduleCreate(ItnScheduleBase):

    pass


# Properties to receive on ItnSchedule update
class ItnScheduleUpdate(ItnScheduleBase):
    pass


# Properties shared by models stored in DB
class ItnScheduleInDBBase(ItnScheduleBase):

    pass


# Properties to return to client
class ItnSchedule(ItnScheduleInDBBase):
    pass
    # meta: ItnMeta

    # Properties properties stored in DB


class ItnScheduleInDB(ItnScheduleInDBBase):
    pass
