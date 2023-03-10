import uuid

from ..services.database import db

from ..core.config import db_config


class SocialAccount(db.Model):
    __tablename__ = 'social_account'
    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'),
                      {'schema': db_config.db})

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(
        db.UUID(as_uuid=True),
        db.ForeignKey(f'{db_config.db}.user.id', ondelete='CASCADE'),
        nullable=False,
    )

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'
