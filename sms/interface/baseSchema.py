from flask_marshmallow import Marshmallow

from .extend import HyperlinkRelated
from ..database import (
    Groups,
    Parts,
    Instruments,
    Pieces,
    Transposes,
    Files
)

ma = Marshmallow()

class GroupBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Groups
        include_fk = False
        include_relationships = False
        load_instance = True

class PartBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Parts
        include_fk = False
        include_relationships = False
        load_instance = True

class InstrumentBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Instruments
        include_fk = False
        include_relationships = False
        load_instance = True

class PieceBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pieces
        include_fk = False
        include_relationships = False
        load_instance = True

class TransposeBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transposes
        include_fk = False
        include_relationships = False
        load_instance = True

class FileBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Files
        include_fk = False
        include_relationships = False
        load_instance = True