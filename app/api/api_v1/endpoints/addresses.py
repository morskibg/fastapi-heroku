from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Address])
def read_addresses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve addresses.
    """
    addresses = crud.address.get_multi(db, skip=skip, limit=limit)

    return addresses


@router.get("/{address_id}", response_model=schemas.Address)
def read_address_by_id(
    address_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve address by id.
    """
    address = crud.address.get(db, id=address_id)
    if not address:
        raise HTTPException(
            status_code=404,
            detail="The address with this id does not exist in the system",
        )

    return address


@router.post("/", response_model=schemas.Address)
def create_address(
    *,
    db: Session = Depends(deps.get_db),
    address_in: schemas.AddressCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new address.
    """
    address = crud.address.create(
        db=db, obj_in=address_in)
    return address


@router.put("/{address_id}", response_model=schemas.Address)
def update_address(
    *,
    db: Session = Depends(deps.get_db),
    address_id: int,
    address_in: schemas.AddressUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an address.
    """
    address = crud.address.get(db=db, id=address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    address = crud.address.update(db=db, db_obj=address, obj_in=address_in)
    return address


@router.delete("/{address_id}", response_model=schemas.Address)
def delete_address(
    *,
    db: Session = Depends(deps.get_db),
    address_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an address.
    """
    address = crud.address.get(db=db, id=address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    address = crud.address.remove(db=db, id=address_id)
    return address
