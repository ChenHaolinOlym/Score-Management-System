from flask_marshmallow import Marshmallow

from .extend import HyperlinkRelated
from ..database import (
    Groups,
    Parts,
    Instruments,
    Pieces,
    Versions,
    Transposes,
    Files
)

ma = Marshmallow()

class GroupBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Groups
        include_relationships = False
        load_instance = True

class PartBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Parts
        include_relationships = False
        load_instance = True

class InstrumentBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Instruments
        include_relationships = False
        load_instance = True

class PieceBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pieces
        include_relationships = False
        load_instance = True

class VersionBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Versions
        include_relationships = False
        load_instance = True

class TransposeBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transposes
        include_relationships = False
        load_instance = True

class FileBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Files
        include_relationships = False
        load_instance = True

class PartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Parts
        include_relationships = True
        load_instance = True

    # instruments = ma.List(HyperlinkRelated("One", "instrument_api"))
    instruments = ma.Nested(InstrumentBaseSchema, many=True)

class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Groups
        include_relationships = True
        load_instance = True

    parts = ma.Nested(PartSchema, many=True)
    pieces = ma.List(HyperlinkRelated("Many", "piece_api"))

class InstrumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Instruments
        include_relationships = True
        load_instance = True

    versions = ma.List(HyperlinkRelated("Many", "version_api"))
    files = ma.List(HyperlinkRelated("Many", "file_api"))

class VersionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Versions
        include_relationships = True
        load_instance = True

class PieceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pieces
        include_relationships = True
        load_instance = True

    versions = ma.Nested(VersionSchema, many=True)

class TransposeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transposes
        include_relationships = True
        load_instance = True

class FileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Files
        include_relationships = True
        load_instance = True