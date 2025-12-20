import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.index'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.models import User
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app