import os

from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from db import db
import model


def create_app(db_url=None):
    app = Flask(__name__)

    username = "sa"
    password = "123"
    host = "localhost"
    database = "estudospython"
    driver = "ODBC Driver 17 for SQL Server"
    database_url = f"mssql+pyodbc://{username}:{password}@{host}/{database}?driver={driver}"

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Rest API para Lojas"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
