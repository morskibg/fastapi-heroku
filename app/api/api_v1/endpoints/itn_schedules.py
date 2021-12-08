from typing import Any, List
import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.utils import convert_date_to_utc_with_hours, convert_date_from_utc

router = APIRouter()


@router.get("/", response_model=List[schemas.ItnSchedule])
def read_schedule(
    db: Session = Depends(deps.get_db),
    startDate: str = '01/01/2021',
    endDate: str = '31/12/2021',
    current_user: models.User = Depends(deps.get_current_active_user),

) -> Any:
    """
    Retrieve itn_schedule.
    """

    try:
        start_date_obj = dt.datetime.strptime(startDate, '%d/%m/%Y')
        end_date_obj = dt.datetime.strptime(endDate, '%d/%m/%Y')
        end_date_obj = end_date_obj.replace(hour=23)

        start_date_utc = convert_date_to_utc_with_hours(
            'Europe/Sofia', start_date_obj)
        end_date_utc = convert_date_to_utc_with_hours(
            'Europe/Sofia', end_date_obj)

        print(start_date_utc, end_date_utc)
        schedules = crud.itn_schedule.get_unique_itn_schedule_for_period_utc(
            db,  start_date=start_date_utc, end_date=end_date_utc)
    except Exception as e:
        print("🚀 ~ file: itn_schedules.py ~ line 40 ~ e", e)
        raise HTTPException(
            status_code=404,
            detail="Wrong query params.",
        )

    return schedules


@router.get("/{itn_id}", response_model=List[schemas.ItnSchedule])
def read_schedule_by_id(
    itn_id: str,
    start_date: str = None,
    end_date: str = None,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve metas by id or id and dates. 
    """
    print(f'in xhedules', itn_id, start_date, end_date)
    if start_date and end_date:
        print('gggggggggggg')
        try:
            start_date_obj = dt.datetime.strptime(start_date, '%d/%m/%Y')
            end_date_obj = dt.datetime.strptime(end_date, '%d/%m/%Y')
            end_date_obj = end_date_obj.replace(hour=23)

            start_date_utc = convert_date_to_utc_with_hours(
                'Europe/Sofia', start_date_obj)
            end_date_utc = convert_date_to_utc_with_hours(
                'Europe/Sofia', end_date_obj)

            print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',
                  start_date_utc, end_date_utc)
            schedules = crud.itn_schedule.get_schedule_by_itn_for_period_utc(
                db, itn=itn_id, start_date=start_date_utc, end_date=end_date_utc)

        except Exception as e:
            print("🚀 ~ file: itn_schedules.py ~ line 58 ~ e", e)
            raise HTTPException(
                status_code=404,
                detail="Wrong query params.",
            )
    else:
        schedules = crud.itn_schedule.get_schedule_by_id(db, itn=itn_id)

    # if not schedules:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="The ITN with this id does not exist in the system",
    #     )

    print("🚀 ~ DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
          len(schedules))
    return schedules


@router.post("/", response_model=schemas.ItnSchedule)
def create_itn_meta(
    *,
    db: Session = Depends(deps.get_db),
    meta_in: schemas.ItnScheduleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new meta.
    """
    itn_meta = crud.itn_meta.create(
        db=db, obj_in=meta_in)
    return itn_meta


@router.put("/{itn_id}", response_model=schemas.ItnSchedule)
def update_contract(
    *,
    db: Session = Depends(deps.get_db),
    itn_id: str,
    meta_in: schemas.ItnScheduleUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an contract.
    """
    itn_meta = crud.itn_meta.get(db=db, id=itn_id)
    if not itn_meta:
        raise HTTPException(status_code=404, detail="ItnSchedule not found")

    itn_meta = crud.itn_meta.update(
        db=db, db_obj=itn_meta, obj_in=meta_in)
    return itn_meta


@router.delete("/{itn_id}", response_model=schemas.ItnSchedule)
def delete_contract(
    *,
    db: Session = Depends(deps.get_db),
    itn_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an contract.
    """
    itn_meta = crud.itn_meta.get(db=db, id=itn_id)
    if not itn_meta:
        raise HTTPException(status_code=404, detail="ItnSchedule not found")

    itn_meta = crud.itn_meta.remove(db=db, id=itn_id)
    return itn_meta

# @router.get("/test/{date}")
