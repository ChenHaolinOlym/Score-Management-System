from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

def create_everything(app:Flask, db:SQLAlchemy) -> None:
    logger = logging.getLogger(__name__)
    with app.app_context():
        # Create database with model
        db.create_all()
        logger.info("Create database by config")

        # TODO: Load base settings


        # TODO: Execute creates