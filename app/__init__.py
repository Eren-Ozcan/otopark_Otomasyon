from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime, date

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.main import main as main_bp
    from app.routes.auth import auth as auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Template filter: Tarih biçimlendirme (gg.aa.yyyy)
    @app.template_filter("format_date")
    def format_date(value):
        if isinstance(value, (datetime, date)):
            return value.strftime("%d.%m.%Y %H:%M:%S")

        return value

    return app
