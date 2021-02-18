from flask import current_app
from flask_sqlalchemy import SQLAlchemy
import logging
from .model import (
    Groups,
    Parts,
    Instruments,
    Pieces,
    Transposes,
    Files
)

def create_everything(db:SQLAlchemy) -> None:
    logger = logging.getLogger(__name__)
    with current_app.app_context():
        # Create database with model
        # TODO: Clear this
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
        file1 = Files(format="format", filename="1")
        file2 = Files(format="format", filename="2")
        file3 = Files(format="format", filename="3")
        file4 = Files(format="format", filename="4")
        file5 = Files(format="format", filename="5")
        transpose1 = Transposes(from_bar=1, to_bar=2, from_instrument=instrument1, to_instrument=instrument1)
        transpose2 = Transposes(from_bar=3, to_bar=4, from_instrument=instrument2, to_instrument=instrument2)
        transpose3 = Transposes(from_bar=5, to_bar=6, from_instrument=instrument3, to_instrument=instrument3)
        transpose4 = Transposes(from_bar=7, to_bar=8, from_instrument=instrument4, to_instrument=instrument4)
        transpose5 = Transposes(from_bar=9, to_bar=10, from_instrument=instrument5, to_instrument=instrument5)
        piece1 = Pieces(name="piece1", author="author1", lyricist="lyricist1", arranger="arranger1", opus=1)
        piece2 = Pieces(name="piece2", author="author2", lyricist="lyricist2", arranger="arranger2", opus=2)
        piece1.transposes = [transpose1, transpose2, transpose3]
        piece2.transposes = [transpose4, transpose5]
        piece1.files = [file1, file2]
        piece2.files = [file3, file4, file5]
        piece1.groups.append(group)
        piece2.groups.append(group)

        db.session.add(group)
        db.session.add(piece1)
        db.session.add(piece2)
        db.session.commit()


        logger.info("Create database by config")

        # TODO: Load base settings


        # TODO: Execute creates