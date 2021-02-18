from flask import Flask, render_template, jsonify
import os

from .logger import init_logger
from .database import db, create_everything
from .interface import ma, api, register_bluprints

def create_app(config:str=None) -> Flask:
    app = Flask(__name__)

    # Load configs
    if config:
        app.config.from_json(config)
    # TODO: Add something to check whether a file folder is a file folder
    # TODO: Reaction if no config

    # Sqlalchemy Configs
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.config['DB']['FILE']}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # api configs
    app.config['API_TITLE'] = 'SMS API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'

    # initiallize logger
    init_logger(app)

    # initiallize database
    db.init_app(app)

    # initiallize Marshmallow
    ma.init_app(app)

    # Check whether database exists or not
    if not os.path.exists(os.path.join("sms", app.config['DB']['FILE'])):
        app.app_context().push()
        create_everything(db)

    # initiallize api
    api.init_app(app)
    register_bluprints()

    # Error handlers
    # TODO: Modify here
    # @app.errorhandler(ApiGeneralException)
    def general_error_handler(e) -> str:
        if e.code == 500:
            db.session.rollback()
        return jsonify(e.to_dict()), e.code

    # Routes
    @app.route('/')
    def index():
        return render_template("index.html")

    return app