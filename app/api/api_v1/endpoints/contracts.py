from typing import Any, List
import sys

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.utils import create_schedule_dates_from_local
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
    print("🚀 ~ file: contracts.py ~ line 51 ~ contract_in", contract_in)
    try:
        schedule_start_date_utc, schedule_end_date_utc = create_schedule_dates_from_local(
            contract_in.start_date, contract_in.end_date)
        print("🚀 ~ file: contracts.py ~ line 60 ~ schedule_start_date_utc",
              schedule_start_date_utc)

        if not schedule_start_date_utc and not schedule_end_date_utc:
            raise HTTPException(
                status_code=404,
                detail="The dates are in incorrect format !",
            )

      # ADDRESS
        address = crud.address.filter_by_all(db,
                                             city=contract_in.contractor_city,
                                             postal_code=contract_in.contractor_postal_code,
                                             address_line=contract_in.contractor_address_line)
        if not address:
            print('in create new address')
            address = crud.address.create(db, obj_in={'city': contract_in.contractor_city,
                                                      'postal_code': contract_in.contractor_postal_code,
                                                      'address_line': contract_in.contractor_address_line})

      # CONTRACTOR
        contractor = crud.contractor.filter_by_eik(
            db, eik=contract_in.contractor_eik)

        if not contractor:
            print('in create new contractor')
            contractor = crud.contractor.create(
                db,
                obj_in={
                    'name': contract_in.contractor_name,
                    'eik': contract_in.contractor_eik,
                    'address_id': address.id,
                })
        else:
            update_contractor_dict = {}
            if not crud.address.is_match(db, obj_in=address, address_id=contractor.address_id):
                update_contractor_dict['address_id'] = address.id
            elif not crud.contractor.is_match(db, obj_in=contractor, name=contract_in.contractor_name, eik=contract_in.contractor_eik):
                update_contractor_dict['name':contractor.name,
                                       'eik':contractor.eik]
            if bool(update_contractor_dict):
                crud.contractor.update(
                    db, db_obj=contractor, obj_in=update_contractor_dict)
                print(f'in update contractor --> {update_contractor_dict}')

      # CONTRACT
        print('in create new contract')
        contract = crud.contract.create(
            db,
            obj_in={
                'start_date': contract_in.start_date,
                'end_date': contract_in.end_date,
                'contractor_id': contractor.id})

      # ITN

        itn_meta = crud.itn_meta.get_by_id(
            db, id=contract_in.itn)

        meta_address = crud.address.filter_by_all(
            db,
            city=contract_in.itn_city,
            postal_code=contract_in.itn_postal_code,
            address_line=contract_in.itn_address_line)
        if not itn_meta:
            print('in create new meta')
            if not meta_address:
                print('in create new meta_address')
                meta_address = crud.address.create(
                    db,
                    obj_in={'city': contract_in.itn_city,
                            'postal_code': contract_in.itn_postal_code,
                            'address_line': contract_in.itn_address_line})

            itn_meta = crud.itn_meta.create(
                db,
                obj_in={'id': contract_in.itn,
                        'erp': contract_in.erp,
                        'load_type': contract_in.load_type,
                        'address_id': meta_address.id
                        })

        else:
            print('in EXISTING meta')

            schedule = crud.itn_schedule.get_schedule_by_itn_for_period_utc(
                db, itn=contract_in.itn, start_date=schedule_start_date_utc, end_date=schedule_end_date_utc)
            if len(schedule) > 0:
                raise HTTPException(
                    status_code=404, detail=f'Itn {contract_in.itn} has schedule during specified time interval: {contract_in.start_date} - {contract_in.end_date} already ! Correct contract\'s overlapping dates first. ')

      # SubContract create
        sub_contract = crud.sub_contract.create(
            db,
            obj_in={'itn': itn_meta.id,
                    'price': contract_in.price,
                    'start_date': contract_in.start_date,
                    'end_date': contract_in.end_date,
                    'contract_id': contract.id})

        return contract
    except Exception as e:
        print("🚀 ~ file: contracts.py ~ line 97 ~ e", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_type, exc_obj, exc_tb.tb_lineno)
        raise HTTPException(
            status_code=500, detail="Server error ! Contract not created !")


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
