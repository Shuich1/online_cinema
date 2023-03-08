import datetime
import uuid
from sqlalchemy import UniqueConstraint, DDL, event
from dataclasses import dataclass

from src.services.database import db
from src.core.config import db_config


# def create_partition(target, connection, **kw) -> None:
#     """ creating partition by auth_history """
#     connection.execute(
#         """CREATE TABLE IF NOT EXISTS "auth_history_other"
#         PARTITION OF "auth_history" FOR VALUES IN ('other')"""
#     )
#     connection.execute(
#         """CREATE TABLE IF NOT EXISTS "auth_history_mobile"
#         PARTITION OF "auth_history" FOR VALUES IN ('mobile')"""
#     )
#     connection.execute(
#         """CREATE TABLE IF NOT EXISTS "auth_history_web"
#         PARTITION OF "auth_history" FOR VALUES IN ('web')"""
#     )
#     connection.execute(
#             """CREATE TABLE IF NOT EXISTS "auth_history_tablet"
#             PARTITION OF "auth_history" FOR VALUES IN ('tablet')"""
#     )


@dataclass
class AuthHistory(db.Model):
    __tablename__ = 'auth_history'
    __table_args__ = (
            UniqueConstraint('id', 'user_device_type'),
            {
                    'postgresql_partition_by': 'LIST (user_device_type)',
                    'schema': db_config.db
            }

    )

    id: uuid
    user_id: str
    user_agent: str
    host: str
    auth_date: datetime.datetime
    user_device_type: str

    id = db.Column(
        db.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(f'{db_config.db}.user.id'))
    user_agent = db.Column(db.String(255))
    host = db.Column(db.String(255))
    auth_date = db.Column(db.DateTime)
    user_device_type = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.auth_date}>'

# event.listen(
#     AuthHistory.__table__,
#     "after_create",
#     DDL("""CREATE TABLE IF NOT EXISTS "auth_history_other"
#         PARTITION OF "auth_history" FOR VALUES IN ('other')""")
# )


# @event.listens_for(AuthHistory.__table__, "after_create")
