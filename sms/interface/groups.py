from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import fields, Schema

from .extend import HyperlinkRelated
from .baseSchema import ma, GroupBaseSchema, PartBaseSchema, InstrumentBaseSchema
from ..database import Groups

group_blp = Blueprint("groupsApi", __name__,
    url_prefix="/api/groups", description="Api for Groups")

class PartSchema(PartBaseSchema):
    class Meta:
        include_relationships = True
    
    instruments = ma.Nested(InstrumentBaseSchema, many=True)

# class GroupSchema(GroupBaseSchema):
#     class Meta:
#         # TODO: Make a PR about this
#         model = Groups
#         include_relationships = True

#     parts = ma.Nested(PartSchema, many=True)
#     pieces = ma.List(HyperlinkRelated("Many", "piecesApi.all"))

class GroupSchema(GroupBaseSchema):
    class Meta:
        include_fk = True

class GroupQuerySchema(Schema):
    id = fields.Integer()
    name = fields.String()

@group_blp.route("/", endpoint="all")
class GroupsApi(MethodView):

    @group_blp.arguments(GroupQuerySchema, location="query")
    @group_blp.response(schema=GroupSchema(many=True), code=200)
    def get(self, args):
        return Groups.query.filter_by(**args).all()

    def post(self):
        return abort(403)

    def put(self):
        return abort(403)

    def patch(self):
        return abort(403)

    def delete(self):
        return abort(403)

@group_blp.route("/<id>", endpoint="byid")
class GroupsApiById(MethodView):

    @group_blp.arguments(GroupQuerySchema, location="query")
    @group_blp.response(schema=GroupSchema, code=200)
    def get(self, args, id):
        # param id in query string can overide id specified in original url
        id = args.pop("id", False) or id
        return Groups.query.filter_by(id=id, **args).first()

    def post(self, id):
        return abort(403)

    def put(self, id):
        return abort(403)

    def patch(self, id):
        return abort(403)

    def delete(self, id):
        return abort(403)