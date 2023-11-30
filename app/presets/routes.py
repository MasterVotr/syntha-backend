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
    request_data = request.get_json()["preset"]
    print(request_data)
    metadata = request_data["metadata"]
    data = request_data["data"]
    name = metadata["preset_name"]
    creator_id = metadata["creator_id"]
    if User.query.filter_by(id=creator_id).first() is None:
        result = {
            "msg": "Creator user not found",
            "status": HTTPStatus.NOT_FOUND
        }
        return make_response(jsonify(result), result["status"])
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
    result = {
        "result": {
            "preset_id": preset_id
        },
        "status": HTTPStatus.OK
    }
    return make_response(jsonify(result), result["status"])


@bp.route("/<preset_id>", methods=["GET", "DELETE", "POST"])
def modify_preset(preset_id):
    preset = Preset.query.filter_by(id=preset_id).first()
    if preset is None:
        result = {
            "msg": "Preset not found",
            "status": HTTPStatus.NOT_FOUND
        }
        return make_response(jsonify(result), result["status"])

    if request.method == "GET":
        result = {
            "result": {
                "preset": preset
            },
            "status": HTTPStatus.OK
        }
        return make_response(jsonify(result), result["status"])

    elif request.method == "DELETE":
        db.session.delete(preset)
        db.session.commit()
        result = {
            "msg": "Successfully deleted preset",
            "status": HTTPStatus.OK
        }
        return make_response(jsonify(result), result["status"])

    elif request.method == "POST":
        request_data = request.get_json()
        if request_data.get("name"):
            preset.name = request_data.get("name")
        if request_data.get("data"):
            preset.data = request_data.get("data")
        if request_data.get("public"):
            preset.public = int(request_data.get("public"))
        db.session.commit()
        result = {
            "msg": "Successfully updated preset",
            "status": HTTPStatus.OK
        }
        return make_response(jsonify(result), result["status"])


@bp.route("/all", methods=["GET"])
def get_presets():
    presets = Preset.query.all()
    result = {
        "result": presets,
        "status": HTTPStatus.OK
    }
    return make_response(jsonify(result), result["status"])


@bp.route("/public", methods=["GET"])
def get_public_presets():
    presets = Preset.query.all()
    public_presets = []
    for preset in presets:
        if preset.public:
            public_presets.append(preset)
    result = {
        "result": public_presets,
        "status": HTTPStatus.OK
    }
    return make_response(jsonify(result), result["status"])
