from http import HTTPStatus

from flask import render_template, request, redirect, make_response, jsonify
from flask_login import login_user, logout_user, login_required

from app.models.preset import Preset
from app.models.user import User
from app.users import bp
from app.extensions import bcrypt, db


@bp.route("/", methods=["GET"])
def index():
    users = User.query.all()
    return render_template("users/index.html", users=users)


@bp.route("/register", methods=["POST"])
def register():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')

    print(f"username: {username}, password: {password}")

    if User.query.filter_by(username=username).first():
        result = {
            "msg": "Failed: username already exists",
            "status": HTTPStatus.BAD_REQUEST
        }
        return make_response(jsonify(result), result["status"])
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User()
    new_user.username = username
    new_user.password = hashed_password
    new_user.seenTutorial = False
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    result = {
        "user_id": new_user.id,
        "status": HTTPStatus.OK
    }
    return make_response(jsonify(result), result["status"])


@bp.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')

    print(f"username: {username}, password: {password}")

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        result = {
            "result": {
                "user_id": user.id
            },
            "status": HTTPStatus.OK
        }
        return make_response(jsonify(result), result["status"])
    else:
        result = {
            "msg": "Login failed",
            "status": HTTPStatus.BAD_REQUEST
        }
        return make_response(jsonify(result), result["status"])


@bp.route("/logout", methods=["GET"])
def logout():
    logout_user()
    result = {
        "msg": "Successfully logged out",
        "status": HTTPStatus.OK
    }
    return make_response(jsonify(result), result["status"])


@bp.route("/<int:user_id>", methods=["GET", "DELETE", "POST"])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        result = {
            "msg": "user_id not found",
            "status": HTTPStatus.NOT_FOUND
        }
        return make_response(jsonify(result), result["status"])

    if request.method == "GET":
        user_result = extract_user_data(user)
        result = {
            "result": user_result,
            "status": HTTPStatus.OK
        }
        return make_response(jsonify(result), HTTPStatus.OK)

    elif request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        result = {
            "msg": "Successfully deleted user",
            "status": HTTPStatus.OK
        }
        return make_response(jsonify(result), result["status"])

    elif request.method == "POST":
        request_data = request.get_json()
        if request_data.get("username"):
            if (
                User.query.filter_by(id=request_data.get("username")).first()
                is not None
            ):
                result = {
                    "msg": "Failed: username already exists",
                    "status": HTTPStatus.BAD_REQUEST
                }
                return make_response(jsonify(result), result["status"])
            user.username = request_data.get("username")
        if request_data.get("password"):
            user.password = request_data.get("password")
        if request_data.get("seen_tutorial"):
            user.seen_tutorial = request_data.get("seen_tutorial")
        db.session.commit()
        result = {
            "msg": "Successfully updated user",
            "status": HTTPStatus.OK
        }
        return make_response(jsonify(result), result["status"])


@bp.route("/all", methods=["GET"])
def get_users():
    users = User.query.all()
    user_data = []
    for user in users:
        user_data.append(extract_user_data(user))
    result = {
        "result": user_data,
        "status": HTTPStatus.OK
    }
    return make_response(jsonify(result), result["status"])


@bp.route("/<int:user_id>/presets", methods=["GET"])
def get_user_presets(user_id):
    presets = Preset.query.all()
    user_presets = []
    for preset in presets:
        if int(preset.creator_id) == user_id:
            user_presets.append(preset)
    result = {
        "result": user_presets,
        "status": HTTPStatus.OK
    }
    return make_response(jsonify(result), result["status"])


def extract_user_data(user: User):
    return {
        "id": user.id,
        "username": user.username,
        "seen_tutorial": user.seen_tutorial,
    }
