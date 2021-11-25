from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ItnSchedule])
def read_itn_metas(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve itn_metas.
    """
    itn_metas = crud.itn_meta.get_multi(db, skip=skip, limit=limit)

    return itn_metas


@router.get("/{itn_id}", response_model=schemas.ItnSchedule)
def read_itn_meta_by_id(
    itn_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve metas by id.
    """
    itn_meta = crud.itn_meta.get(db, id=itn_id)
    if not itn_meta:
        raise HTTPException(
            status_code=404,
            detail="The ITN with this id does not exist in the system",
        )

    return itn_meta


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