from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Contractor])
def read_addresses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve contractors.
    """
    contractors = crud.contractor.get_multi(db, skip=skip, limit=limit)

    return contractors


@router.get("/{contractor_id}", response_model=schemas.Contractor)
def read_address_by_id(
    contractor_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve contractor by id.
    """
    contractor = crud.contractor.get(db, id=contractor_id)
    if not contractor:
        raise HTTPException(
            status_code=404,
            detail="The contractor with this id does not exist in the system",
        )

    return contractor


@router.post("/", response_model=schemas.Contractor)
def create_address(
    *,
    db: Session = Depends(deps.get_db),
    address_in: schemas.ContractorCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new contractor.
    """
    contractor = crud.contractor.create(
        db=db, obj_in=address_in)
    return contractor


@router.put("/{contractor_id}", response_model=schemas.Contractor)
def update_address(
    *,
    db: Session = Depends(deps.get_db),
    contractor_id: int,
    address_in: schemas.ContractorUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an contractor.
    """
    contractor = crud.contractor.get(db=db, id=contractor_id)
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")

    contractor = crud.contractor.update(
        db=db, db_obj=contractor, obj_in=address_in)
    return contractor


@router.delete("/{contractor_id}", response_model=schemas.Contractor)
def delete_address(
    *,
    db: Session = Depends(deps.get_db),
    contractor_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an contractor.
    """
    contractor = crud.contractor.get(db=db, id=contractor_id)
    if not contractor:
        raise HTTPException(status_code=404, detail="Contractor not found")

    contractor = crud.contractor.remove(db=db, id=contractor_id)
    return contractor
