from flask import Blueprint

bp = Blueprint("presets", __name__)

from app.presets import routes
