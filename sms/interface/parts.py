from flask_marshmallow import schema
from sms.database.model import Files
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import fields, Schema

from ..database import Parts
from .baseSchema import ma, PartBaseSchema, InstrumentBaseSchema

part_blp = Blueprint("partsApi", __name__,
    url_prefix="/api/parts", description="Api for Parts")

# class PartSchema(PartBaseSchema):
#     class Meta:
#         include_relationships = True
    
#     instruments = ma.Nested(InstrumentBaseSchema, many=True)

class PartSchema(PartBaseSchema):
    class Meta:
        model = Parts
        include_fk = True

class PartQuerySchema(Schema):
    id = fields.Integer()
    name = fields.String()

@part_blp.route("/", endpoint="all")
class PartsApi(MethodView):

    @part_blp.arguments(PartQuerySchema, location="query")
    @part_blp.response(schema=PartSchema(many=True), code=200)
    def get(self, args):
        return Parts.query.all()

    def post(self):
        return abort(403)

    def put(self):
        return abort(403)

    def patch(self):
        return abort(403)

    def delete(self):
        return abort(403)

@part_blp.route("/<id>", endpoint="byid")
class PartsApiById(MethodView):

    @part_blp.arguments(PartQuerySchema, location="query")
    @part_blp.response(schema=PartSchema, code=200)
    def get(self, args, id):
        id = args.pop("id", False) or id
        return Parts.query.filter_by(id=id).first()

    def post(self, id):
        return abort(403)

    def put(self, id):
        return abort(403)

    def patch(self, id):
        return abort(403)

    def delete(self, id):
        return abort(403)