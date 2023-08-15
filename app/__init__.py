from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS
from flask_restful import Api

__version__ = "0.0.0"

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    CORS(app)
    print(f"config_name: {config_name}")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    # model imports:
    # from .models.usr import User, Permission, Role
    # from .models.target_settings_model import TargetSettings



    # create and register swagger blueprint:
    from .swagger.swagger_ui import swaggerui_blueprint as sb
    app.register_blueprint(sb)

    # endpoints imports:

    # TEST_ENDPOINTS_START
    # from .deliver_api.test_endpoint import TestEndpoint




    api = Api(app)

    # enpoints resourcen registrieren:

    # api.add_resource(TestEndpoint, "/api/test")



    # blueprints registrieren
    # from app.admin_api import admin_api_bp as admin_api
    # from app.deliver_api import delivery_api_bp as delivery_api

    # app.register_blueprint(admin_api)
    # app.register_blueprint(delivery_api)

    with app.app_context():
        db.create_all()
        # usr.Role.insert_roles()
        db.session.commit()


    return app

# eof
