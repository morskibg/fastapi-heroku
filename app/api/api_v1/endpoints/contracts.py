from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Contract])
def read_contracts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve contracts.
    """
    contracts = crud.contract.get_multi(db, skip=skip, limit=limit)

    return contracts


@router.get("/{contract_id}", response_model=schemas.Contract)
def read_contract_by_id(
    contract_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve contract by id.
    """
    contract = crud.contract.get(db, id=contract_id)
    if not contract:
        raise HTTPException(
            status_code=404,
            detail="The contract with this id does not exist in the system",
        )

    return contract


@router.post("/", response_model=schemas.Contract)
def create_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_in: schemas.ContractCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new contract.
    """
    contract = crud.contract.create(
        db=db, obj_in=contract_in)
    return contract


@router.put("/{contract_id}", response_model=schemas.Contract)
def update_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    contract_in: schemas.ContractUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an contract.
    """
    contract = crud.contract.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract = crud.contract.update(
        db=db, db_obj=contract, obj_in=contract_in)
    return contract


@router.delete("/{contract_id}", response_model=schemas.Contract)
def delete_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an contract.
    """
    contract = crud.contract.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract = crud.contract.remove(db=db, id=contract_id)
    return contract
