# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.itn_meta import ItnMeta  # noqa
from app.models.contract import Contract  # noqa
from app.models.contractor import Contractor  # noqa
from app.models.address import Address  # noqa
from app.models.user import User  # noqa
from app.models.itn_schedule import ItnSchedule  # noqa
