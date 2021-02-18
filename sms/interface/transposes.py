from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import fields, Schema

from .baseSchema import ma, TransposeBaseSchema, InstrumentBaseSchema, PieceBaseSchema
from ..database import db, Transposes

transpose_blp = Blueprint("transposesApi", __name__,
    url_prefix="/api/transposes", description="Api for Transposes")

class TransposeSchema(TransposeBaseSchema):
    class Meta:
        include_relationships = True

    from_instrument = ma.Nested(InstrumentBaseSchema)
    to_instrument = ma.Nested(InstrumentBaseSchema)
    pieces = ma.Nested(PieceBaseSchema)

class TransposeQuerySchema(Schema):
    id = fields.Integer()
    from_bar = fields.Integer()
    to_bar = fields.Integer()
    # TODO: Determine how to deal with instruments input
    from_instrument_id = fields.Integer()
    to_instrument_id = fields.Integer()

class TransposePostSchema(Schema):
    from_bar = fields.Integer()
    to_bar = fields.Integer()
    piece_id = fields.Integer(required=True, error_messages={
        "required": "A transpose should always be attatched to a piece"
    })
    from_instrument_id = fields.Integer(required=True, error_messages={
        "required": "Instrument that is transposed from is required"
    })
    to_instrument_id = fields.Integer(required=True, error_messages={
        "required": "Instrument that is transposed to is required"
    })

class TransposePutSchema(TransposePostSchema):
    id = fields.Integer(required=True, error_messages={
        "required": "id is required when putting data"
    })

class TransposeDeleteSchema(Schema):
    id = fields.Integer(required=True, error_messages={
        "required": "id is required when deleting data"
    })

@transpose_blp.route("/", endpoint="all")
class TransposesApi(MethodView):

    @transpose_blp.arguments(TransposeQuerySchema, location="query")
    @transpose_blp.response(schema=TransposeSchema(many=True), code=200)
    def get(self, args):
        return Transposes.query.filter_by(**args).all()

    @transpose_blp.arguments(TransposePostSchema, location="json")
    @transpose_blp.response(schema=TransposeSchema, code=201)
    def post(self, args):
        transpose = Transposes(**args)
        db.session.add(transpose)
        db.session.commit()
        return transpose

    @transpose_blp.arguments(TransposePutSchema(many=True), location="json")
    @transpose_blp.response(code=204)
    def put(self, args):
        # TODO: Complete the case that a resource can't be found
        for input in args:
            Transposes.query.filter_by(id=input["id"]).update(input)
        db.session.commit()
        return None

    def patch(self, args):
        # TODO: Complete patch
        pass

    @transpose_blp.arguments(TransposeDeleteSchema(many=True), location="json")
    @transpose_blp.response(code=204)
    def delete(self, args):
        for input in args:
            transpose = Transposes.query.filter_by(id=input["id"]).first()
            db.session.delete(transpose)
        db.session.commit()
        return None


@transpose_blp.route("/<id>", endpoint="byid")
class TransposesApiById(MethodView):

    @transpose_blp.arguments(schema=TransposeQuerySchema, location="query")
    @transpose_blp.response(schema=TransposeSchema)
    def get(self, args, id):
        # param id in query string can overide id specified in original url
        # But only the first result would be returned
        id = args.pop("id", False) or id
        return Transposes.query.filter_by(id=id, **args).first()

    def post(self, args, id):
        return abort(403)

    @transpose_blp.arguments(TransposePutSchema, location="json")
    @transpose_blp.response(code=204)
    def put(self, args, id):
        # TODO: Complete the case that a resource can't be found
        id = args.pop("id", False) or id
        Transposes.query.filter_by(id=id).update(args)
        db.session.commit()
        return None

    def patch(self, args, id):
        # TODO: Complete patch
        pass

    @transpose_blp.arguments(TransposeDeleteSchema, location="json")
    @transpose_blp.response(code=204)
    def delete(self, args, id):
        id = args.pop("id", False) or id
        transpose = Transposes.query.filter_by(id=id).first()
        db.session.delete(transpose)
        db.session.commit()
        return None