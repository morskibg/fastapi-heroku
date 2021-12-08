from typing import Any, List
import datetime as dt

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ItnMeta])
def read_itn_metas(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100000,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve itn_metas.   """

    itn_metas = crud.itn_meta.get_multi(db, skip=skip, limit=limit)

    return itn_metas


# @router.get("/{start_date}/{end_date}", response_model=List[schemas.ItnMeta])
# def read_available_itn_metas_by_period(

#     start_date: str,
#     end_date: str,
#     current_user: models.User = Depends(deps.get_current_active_user),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Retrieve availabe (free) metas by time period.
#     """
#     try:
#         start_date_obj = dt.datetime.strptime(start_date, '%d/%m/%Y')
#         end_date_obj = dt.datetime.strptime(end_date, '%d/%m/%Y')
#         print("🚀 ~ file: itn_metas.py ~ line 61 ~ end_date_obj", end_date_obj)
#     except:
#         raise HTTPException(
#             status_code=404,
#             detail="The dates must be in format dd/mm/yyyy .",
#         )

#     metas = crud.itn_meta.get_all_availabe_for_period(
#         db, start_date=start_date, end_date=end_date)

#     return metas


@router.get("/{itn_id}", response_model=schemas.ItnMeta)
def read_itn_meta_by_id(
    itn_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve metas by id.
    """
    itn_meta = crud.itn_meta.get_by_id(db, id=itn_id)
    if not itn_meta:
        raise HTTPException(
            status_code=404,
            detail="The ITN with this id does not exist in the system",
        )

    return itn_meta


@router.post("/", response_model=schemas.ItnMeta)
def create_itn_meta(
    *,
    db: Session = Depends(deps.get_db),
    meta_in: schemas.ItnMetaCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new meta.
    """
    itn_meta = crud.itn_meta.create(
        db=db, obj_in=meta_in)
    return itn_meta


@router.put("/{itn_id}", response_model=schemas.ItnMeta)
def update_contract(
    *,
    db: Session = Depends(deps.get_db),
    itn_id: str,
    meta_in: schemas.ItnMetaUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an contract.
    """
    itn_meta = crud.itn_meta.get(db=db, id=itn_id)
    if not itn_meta:
        raise HTTPException(status_code=404, detail="ItnMeta not found")

    itn_meta = crud.itn_meta.update(
        db=db, db_obj=itn_meta, obj_in=meta_in)
    return itn_meta


@router.delete("/{itn_id}", response_model=schemas.ItnMeta)
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
    print("🚀 ~ file: itn_metas.py ~ line 92 ~ itn_meta", itn_meta)
    if not itn_meta:
        raise HTTPException(status_code=404, detail="ItnMeta not found")

    itn_meta = crud.itn_meta.remove(db=db, id=itn_id)
    print("🚀 ~ file: itn_metas.py ~ line 97 ~ itn_meta", itn_meta)
    return itn_meta
