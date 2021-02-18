from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import fields, Schema

from .baseSchema import ma, PieceBaseSchema, GroupBaseSchema
from ..database import db, Pieces, Groups, Instruments, Transposes

piece_blp = Blueprint("piecesApi", __name__,
    url_prefix="/api/pieces", description="Api for Pieces")

# class PieceSchema(PieceBaseSchema):
#     class Meta:
#         include_relationships = True

#     groups = ma.Nested(GroupBaseSchema, many=True)

class PieceSchema(PieceBaseSchema):
    class Meta:
        include_fk = True

    # groups = ma.Nested(GroupBaseSchema, many=True)

class PieceQuerySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    author = fields.String()
    lyricist = fields.String()
    arranger = fields.String()
    opus = fields.Integer()
    copyright_expire_date = fields.Date()

class PiecePostSchema(Schema):
    name = fields.String(required=True, error_messages={
        "required": "Name is required"
    })
    author = fields.String()
    lyricist = fields.String()
    arranger = fields.String()
    opus = fields.Integer()
    copyright_expire_date = fields.Date()
    group_ids = fields.List(fields.Integer())
    

@piece_blp.route("/", endpoint="all")
class PiecesApi(MethodView):

    @piece_blp.arguments(PieceQuerySchema, location="query")
    @piece_blp.response(PieceSchema(many=True), code=200)
    def get(self, args):
        return Pieces.query.filter_by(**args).all()

    @piece_blp.arguments(PiecePostSchema, location="json")
    @piece_blp.response(PieceSchema, code=201)
    def post(self, args):
        group_ids = args.pop("group_ids", None)
        piece = Pieces(**args)
        if group_ids:
            groups = []
            for group_id in group_ids:
                group = Groups.query.filter_by(id=group_id).first()
                groups.append(group)
            piece.groups.extend(groups)
        db.session.add(piece)
        db.session.commit()
        return piece

    def put(self, args):
        pass

    def patch(self, args):
        pass

    def delete(self, args):
        pass


@piece_blp.route("/<id>", endpoint="byid")
class PiecesApiById(MethodView):

    @piece_blp.arguments(PieceQuerySchema, location="query")
    @piece_blp.response(PieceSchema, code=200)
    def get(self, args, id):
        # param id in query string can overide id specified in original url
        # But only the first result would be returned
        id = args.pop("id", False) or id
        return Pieces.query.filter_by(id=id, **args).first()

    def post(self, id):
        return abort(403)

    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass
