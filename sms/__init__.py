from flask import Flask, render_template
from flask.json import jsonify

from .database import db
from .interface import api, ApiGeneralException

def create_app(config:str=None) -> Flask:
    app = Flask(__name__)
    
    if config:
        app.config.from_json(config)
    
    # Sqlalchemy Configs
    # TODO: Check info in config and tehn add flask config
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.config['DB_DIRECTORY']}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initiallize database
    db.init_app(app)
    # TODO: Check whether db exists, if not, print a warning and create a new one here

    # initiallize api
    api.init_app(app)

    # Error handlers
    @app.errorhandler(ApiGeneralException)
    def general_error_handler(e) -> str:
        if e.code == 500:
            db.session.rollback()
        return jsonify(e.to_dict()), e.code

    # Routes
    @app.route('/')
    def index():
        return render_template("index.html")

    return app