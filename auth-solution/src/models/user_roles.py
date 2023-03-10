import uuid

from ..services.database import db
from ..core.config import db_config

db.metadata.schema = db_config.db
roles_users = db.Table(
        "roles_users",
        db.metadata,
        db.Column('id',
                  db.UUID(as_uuid=True),
                  primary_key=True,
                  default=uuid.uuid4,
                  unique=True,
                  nullable=False
                  ),
        db.Column('user_id', db.UUID(as_uuid=True)),
        db.Column('role_id', db.UUID(as_uuid=True), db.ForeignKey(f'{db_config.db}.role.id')),
        db.Column('email', db.String(255)),
        db.ForeignKeyConstraint(('user_id', 'email'),
                                (f'{db_config.db}.user.id',
                                 f'{db_config.db}.user.email'))
)
