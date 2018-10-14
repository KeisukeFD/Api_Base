from datetime import datetime
from app import db


class TimestampMixin(object):
    created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)


class AuditMixin(object):
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
