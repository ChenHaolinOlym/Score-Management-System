from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from .model import (
    Groups,
    Parts,
    Instruments
)

def create_everything(app:Flask, db:SQLAlchemy) -> None:
    logger = logging.getLogger(__name__)
    with app.app_context():
        # Create database with model
        db.create_all()
        group = Groups(name="name")
        part1 = Parts(name="as")
        part2 = Parts(name="as2")
        instrument1 = Instruments(name="Hello1")
        instrument2 = Instruments(name="Hello2")
        instrument3 = Instruments(name="Hello3")
        instrument4 = Instruments(name="Hello4")
        instrument5 = Instruments(name="Hello5")
        part1.instruments = [instrument1, instrument2]
        part2.instruments = [instrument3, instrument4, instrument5]
        group.parts = [part1, part2]



        db.session.add(group)
        db.session.commit()


        logger.info("Create database by config")

        # TODO: Load base settings


        # TODO: Execute creates