from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.config.from_object(config_class)

    db.init_app(app)

    app.secret_key = os.urandom(24)

    # ブループリントの登録
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
