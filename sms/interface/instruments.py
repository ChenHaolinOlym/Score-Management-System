from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import fields, Schema

from ..database import Instruments
from .baseSchema import InstrumentBaseSchema

instrument_blp = Blueprint("insturmentApi", __name__,
    url_prefix="/api/instruments", description="Api for Instruments")

class InstrumentSchema(InstrumentBaseSchema):
    class Meta:
        model = Instruments
        include_fk = True

class InstrumentQuerySchema(Schema):
    id = fields.Integer()
    name = fields.String()

@instrument_blp.route("/", endpoint="all")
class InstrumentsApi(MethodView):

    @instrument_blp.arguments(InstrumentQuerySchema, location="query")
    @instrument_blp.response(schema=InstrumentSchema(many=True), code=200)
    def get(self, args):
        return Instruments.query.all()

    def post(self):
        return abort(403)

    def put(self):
        return abort(403)

    def patch(self):
        return abort(403)

    def delete(self):
        return abort(403)

@instrument_blp.route("/<id>", endpoint="byid")
class InstrumentApiById(MethodView):

    @instrument_blp.arguments(InstrumentQuerySchema, location="query")
    @instrument_blp.response(schema=InstrumentSchema, code=200)
    def get(self, args, id):
        id = args.pop("id", False) or id
        return Instruments.query.filter_by(id=id).first()

    def post(self, id):
        return abort(403)

    def put(self, id):
        return abort(403)

    def patch(self, id):
        return abort(403)

    def delete(self, id):
        return abort(403)