from dataclasses import dataclass

from flask_login import UserMixin

from app.extensions import db


@dataclass
class User(db.Model, UserMixin):
    id: int
    username: str
    password: str
    seen_tutorial: int

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    seen_tutorial = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User "{self.username}">'
