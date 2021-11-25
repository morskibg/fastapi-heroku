# from .crud_item import item
from .crud_user import user
from .crud_address import address
from .crud_contractor import contractor
from .crud_contract import contract
from .crud_itn_meta import itn_meta
from .crud_itn_schedule import itn_schedule

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
