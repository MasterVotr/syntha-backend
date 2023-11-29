import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_LEY = os.environ.get("SECRET_KEY") or "FJR-secret1324"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "syntha_db.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
