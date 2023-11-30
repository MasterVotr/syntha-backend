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


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if User.query.filter_by(username=username).first():
            return make_response(
                "Failed: username already exists", HTTPStatus.BAD_REQUEST
            )
        hashed_password = bcrypt.generate_password_hash(password)
        new_user = User()
        new_user.username = username
        new_user.password = hashed_password
        new_user.seenTutorial = False
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return make_response(
            f"Successfully registered and logged in as {username}",
            HTTPStatus.OK,
            {"user_id": new_user.id},
        )
    else:
        return """
                  <form method="POST">
                      <div><label>username: <input type="text" name="username"></label></div>
                      <div><label>password: <input type="password" name="password"></label></div>
                      <input type="submit" value="Submit">
                  </form>"""


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return make_response(f"Successfully loggen in as {username}", HTTPStatus.OK)
        else:
            return make_response("Login failed", HTTPStatus.BAD_REQUEST)
    else:
        return """
                      <form method="POST">
                          <div><label>username: <input type="text" name="username"></label></div>
                          <div><label>password: <input type="password" name="password"></label></div>
                          <input type="submit" value="Submit">
                      </form>"""


@bp.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return make_response("Successfully logged out", HTTPStatus.OK)


@bp.route("/<int:user_id>", methods=["GET", "DELETE", "POST"])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response("User not found", HTTPStatus.NOT_FOUND)

    if request.method == "GET":
        user_result = {
            "id": user.id,
            "username": user.username,
            "seen_tutorial": user.seen_tutorial,
        }
        return make_response(jsonify(user_result), HTTPStatus.OK)

    elif request.method == "DELETE":
        db.session.delete(user)
        db.session.commit()
        return make_response("Successfully deleted user", HTTPStatus.OK)

    elif request.method == "POST":
        request_data = request.get_json()
        if request_data.get("username"):
            if (
                User.query.filter_by(id=request_data.get("username")).first()
                is not None
            ):
                return make_response(
                    "Failed: username already exists", HTTPStatus.BAD_REQUEST
                )
            user.username = request_data.get("username")
        if request_data.get("password"):
            user.password = request_data.get("password")
        if request_data.get("seen_tutorial"):
            user.seen_tutorial = request_data.get("seen_tutorial")
        db.session.commit()
        return make_response("Successfully updated user", HTTPStatus.OK)


@bp.route("/all", methods=["GET"])
def get_users():
    users = User.query.all()
    return make_response(jsonify(users), HTTPStatus.OK)


@bp.route("/<int:user_id>/presets", methods=["GET"])
def get_user_presets(user_id):
    presets = Preset.query.all()
    user_presets = []
    for preset in presets:
        if int(preset.creator_id) == user_id:
            user_presets.append(preset)
    return make_response(jsonify(user_presets), HTTPStatus.OK)
