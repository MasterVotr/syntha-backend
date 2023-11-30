from http import HTTPStatus

from flask_login import login_user

from app.models.preset import Preset
from app.models.user import User
from app.extensions import bcrypt, db


class UserService:
    def __int__(self):
        pass

    def register_user(self, params):
        username = params.get("username")
        password = params.get("password")

        if User.query.filter_by(username=username).first():
            raise HTTPStatus.BAD_REQUEST

        hashed_password = bcrypt.generate_password_hash(password)
        new_user = User()
        new_user.username = username
        new_user.password = hashed_password
        new_user.seenTutorial = False
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return new_user.id

    def login_user(self, params):
        username = params.get("username")
        password = params.get("password")

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return user.id
        else:
            raise HTTPStatus.BAD_REQUEST

    def update_user(self, user_id, params):
        user = self.get_user()
        new_username = params.get("username")
        if new_username:
            if User.query.filter_by(username=new_username).first() is not None:
                raise HTTPStatus.BAD_REQUEST
            user.username = params.get("username")
        if params.get("password"):
            user.password = params.get("password")
        if params.get("seen_tutorial"):
            user.seen_tutorial = params.get("seen_tutorial")
        db.session.commit()

    def delete_user(self, user_id):
        db.session.delete(self.get_user(user_id))
        db.session.commit()

    def get_user(self, user_id):
        return self.extract_user_data(User.query.filter_by(id=user_id).first())

    def get_users(self):
        users = User.query.all()
        user_data = []
        for user in users:
            user_data.append(self.extract_user_data(user))
        return users

    def get_user_presets(self, user_id):
        presets = Preset.query.all()
        user_presets = []
        for preset in presets:
            if int(preset.creator_id) == user_id:
                user_presets.append(preset)
        return user_presets

    def check_exists_user(self, user_id):
        User.query.filter_by(id=user_id).first_or_404()

    def extract_user_data(self, user: User):
        return {
            "id": user.id,
            "username": user.username,
            "seen_tutorial": user.seen_tutorial,
        }
