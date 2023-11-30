import datetime
from dataclasses import dataclass

from sqlalchemy import ForeignKey

from app.extensions import db


@dataclass
class Preset(db.Model):
    id: int
    name: str
    public: int
    data: str
    creator_id: int
    date_created: datetime.datetime

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    public = db.Column(db.Integer, default=1)
    data = db.Column(db.Text)
    creator_id = db.Column(ForeignKey("user.id"), nullable=False)
    date_created = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Preset {self.name}>"
