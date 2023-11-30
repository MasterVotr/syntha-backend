from flask import Flask

from app.models.user import User
from config import Config
from app.extensions import db, bcrypt, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extension
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.presets import bp as presets_bp

    app.register_blueprint(presets_bp, url_prefix="/presets")

    from app.users import bp as users_bp

    app.register_blueprint(users_bp, url_prefix="/users")

    @app.route("/test/")
    def test_page():
        return "<h1>Testing the Application Factory</h1>"

    return app
