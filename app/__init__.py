import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    # Falls back to a development key so a fresh clone still starts, but a real
    # deployment must set SECRET_KEY: sessions signed with a key published in
    # this repository can be forged by anyone who reads it.
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-insecure-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///site.db'
    )

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # Without this, Flask-Login cannot restore a session and every
        # @login_required route bounces to the login page forever.
        return db.session.get(User, int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .recipes import recipes as recipes_blueprint
    app.register_blueprint(recipes_blueprint)

    from .meal_plan import meal_plan as meal_plan_blueprint
    app.register_blueprint(meal_plan_blueprint)

    with app.app_context():
        db.create_all()

    return app
