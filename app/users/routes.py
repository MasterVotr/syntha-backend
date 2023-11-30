from http import HTTPStatus

from flask import render_template, request, redirect, make_response, jsonify
from flask_login import login_user, logout_user, login_required

from app.models.preset import Preset
from app.models.user import User
from app.services import user_service
from app.users import bp
from app.extensions import bcrypt, db



@bp.route("/", methods=["GET"])
def index():
    users = user_service.get_users()
    return render_template("users/index.html", users=users)


@bp.route("/register", methods=["POST"])
def register():
    request_data = request.get_json()

    try:
        new_user_id = user_service.register_user(request_data)
    except HTTPStatus.BAD_REQUEST:
        result = {
            "msg": "Failed: username already exists",
            "status": HTTPStatus.BAD_REQUEST,
        }
        return make_response(jsonify(result), result["status"])

    result = {"user_id": new_user_id, "status": HTTPStatus.OK}
    return make_response(jsonify(result), result["status"])


@bp.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()

    try:
        user_id = user_service.login_user(request_data)
    except HTTPStatus.BAD_REQUEST:
        result = {"msg": "Login failed", "status": HTTPStatus.BAD_REQUEST}
        return make_response(jsonify(result), result["status"])

    result = {"result": {"user_id": user_id}, "status": HTTPStatus.OK}
    return make_response(jsonify(result), result["status"])


@bp.route("/logout", methods=["GET"])
def logout():
    logout_user()
    result = {"msg": "Successfully logged out", "status": HTTPStatus.OK}
    return make_response(jsonify(result), result["status"])


@bp.route("/<int:user_id>", methods=["GET", "DELETE", "POST"])
def update_user(user_id):
    try:
        user_service.check_exists_user(user_id)
    except HTTPStatus.NOT_FOUND:
        result = {"msg": "user_id not found", "status": HTTPStatus.NOT_FOUND}
        return make_response(jsonify(result), result["status"])

    if request.method == "GET":
        user_result = user_service.get_user(user_id)
        result = {"result": user_result, "status": HTTPStatus.OK}
        return make_response(jsonify(result), HTTPStatus.OK)

    elif request.method == "DELETE":
        user_service.delete_user(user_id)
        result = {"msg": "Successfully deleted user", "status": HTTPStatus.OK}
        return make_response(jsonify(result), result["status"])

    elif request.method == "POST":
        request_data = request.get_json()
        try:
            user_service.update_user(user_id, request_data)
        except HTTPStatus.BAD_REQUEST:
            result = {
                "msg": "Failed: username already exists",
                "status": HTTPStatus.BAD_REQUEST,
            }
            return make_response(jsonify(result), result["status"])
        result = {"msg": "Successfully updated user", "status": HTTPStatus.OK}
        return make_response(jsonify(result), result["status"])


@bp.route("/all", methods=["GET"])
def get_users():
    users = user_service.get_users()
    result = {"result": users, "status": HTTPStatus.OK}
    return make_response(jsonify(result), result["status"])


@bp.route("/<int:user_id>/presets", methods=["GET"])
def get_user_presets(user_id):
    user_presets = user_service.get_user_presets(user_id)
    result = {"result": user_presets, "status": HTTPStatus.OK}
    return make_response(jsonify(result), result["status"])
