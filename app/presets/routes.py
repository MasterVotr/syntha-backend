import sys
from datetime import timezone, datetime
from http import HTTPStatus
from json import dumps

from flask import render_template, request, make_response, jsonify

from app import db
from app.models.preset import Preset
from app.models.user import User
from app.presets import bp


@bp.route("/")
def index():
    presets = Preset.query.all()
    return render_template("presets/index.html", presets=presets)


@bp.route("/new", methods=["POST"])
def create():
    request_data = request.get_json()
    print(request_data)
    metadata = request_data["metadata"]
    data = request_data["data"]
    name = metadata["name"]
    creator_id = metadata["creator_id"]
    if User.query.filter_by(id=creator_id).first() is None:
        return make_response("Creator user not found", HTTPStatus.NOT_FOUND)
    public = metadata["public"]

    new_preset = Preset()
    new_preset.name = name
    new_preset.public = public
    new_preset.creator_id = creator_id
    new_preset.date_created = datetime.now(timezone.utc)
    new_preset.data = dumps(data)
    db.session.add(new_preset)
    db.session.commit()

    preset_id = new_preset.id
    return make_response(
        "Preset successfully created/updated", HTTPStatus.OK, {"preset_id": preset_id}
    )


@bp.route("/<preset_id>", methods=["GET", "DELETE", "POST"])
def modify_preset(preset_id):
    preset = Preset.query.filter_by(id=preset_id).first()
    if preset is None:
        return make_response("Preset not found", HTTPStatus.NOT_FOUND)

    if request.method == "GET":
        return make_response(jsonify(preset), HTTPStatus.OK)

    elif request.method == "DELETE":
        db.session.delete(preset)
        db.session.commit()
        return make_response("Successfully deleted preset", HTTPStatus.OK)

    elif request.method == "POST":
        request_data = request.get_json()
        if request_data.get("name"):
            preset.name = request_data.get("name")
        if request_data.get("data"):
            preset.data = request_data.get("data")
        if request_data.get("public"):
            preset.public = int(request_data.get("public"))
        db.session.commit()
        return make_response("Successfully updated preset", HTTPStatus.OK)


@bp.route("/all", methods=["GET"])
def get_presets():
    presets = Preset.query.all()
    return make_response(jsonify(presets), HTTPStatus.OK)


@bp.route("/public", methods=["GET"])
def get_public_presets():
    presets = Preset.query.all()
    public_presets = []
    for preset in presets:
        if preset.public:
            public_presets.append(preset)
    return make_response(jsonify(public_presets), HTTPStatus.OK)
