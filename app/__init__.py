"""Microservice Package."""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config import config

from internal.errors import HTTPException

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name="default"):
    """Create Flask object called app and return it."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(HTTPException)
    def custom_error(exception):
        response = jsonify(exception.error_response.error_dict)
        response.status_code = exception.status_code
        return response

    from .main.views import main_blueprint
    app.register_blueprint(main_blueprint)
    from .user.views import user_blueprint
    app.register_blueprint(user_blueprint)

    return app
