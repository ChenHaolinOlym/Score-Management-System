from flask_marshmallow import Marshmallow

from .model import (
    Groups,
    Parts,
    Instruments,
    Pieces,
    Versions,
    Transposes,
    Files
)

ma = Marshmallow()

# TODO: Add hyperlink representation after enpoints in apis are settled

class GroupsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Groups
        include_fk = True
        load_instance = True

class PartsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Parts
        include_fk = True
        load_instance = True

class InstrumentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Instruments
        include_fk = True
        load_instance = True

class PiecesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pieces
        include_fk = True
        load_instance = True

class VersionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Versions
        include_fk = True
        load_instance = True

class TransposesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transposes
        include_fk = True
        load_instance = True

class FilesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Files
        include_fk = True
        load_instance = True