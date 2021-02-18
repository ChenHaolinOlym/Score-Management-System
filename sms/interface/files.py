import os
from flask import current_app, send_from_directory, send_file
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_smorest.fields import Upload
from marshmallow import fields, Schema
from werkzeug.utils import secure_filename

from .baseSchema import ma, FileBaseSchema
from ..database import db, Files, Pieces, Instruments

file_blp = Blueprint("filesApi", __name__,
    url_prefix="/api/files", description="Api for Files")

# Helper functions
def get_full_filename(filename, format):
    return filename + "." + format

class FileSchema(FileBaseSchema):
    class Meta:
        include_relationships = True

class FileQuerySchema(Schema):
    format = fields.String()
    filename = fields.String()

class FileUploadSchema(Schema):
    file = Upload(required=True, error_messages={
        "required": "A file should be attached"
    })

class FilePostSchema(Schema):
    instrument_id = fields.List(fields.Integer(), required=True, error_messages={
        "required": "An array of instrument ids should be provided"
    })
    piece_id = fields.Integer(required=True, error_messages={
        "required": "A piece id of the file should be provided"
    })

@file_blp.route("/", endpoint="all")
class FilesApi(MethodView):

    @file_blp.arguments(FileQuerySchema, location="query")
    @file_blp.response(FileSchema(many=True), code=200)
    def get(self, args):
        return Files.query.filter_by(**args).all()

    @file_blp.arguments(FileUploadSchema, location="files")
    @file_blp.arguments(FilePostSchema, location="form")
    @file_blp.response(schema=FileSchema, code=201)
    def post(self, files, args):
        # TODO: Try to provide multiple file upload in one post
        # By adding file1, file2, file3 as optional
        # TODO: Check whether a file and filename is exist and ways to avoid
        # TODO: Find a way to upload multiple instrument id in one time
        file = files["file"]
        mimetype = file.content_type.split("/")[1]

        piece = Pieces.query.filter_by(id=args["piece_id"]).first()
        file_db = Files()
        
        instruments_name = ""
        for instrument_id in args["instrument_id"]:
            instrument = Instruments.query.filter_by(id=instrument_id).first()
            file_db.instruments.append(instrument)
            instruments_name += instrument.name
        
        file_db.piece = piece
        filename = secure_filename(piece.name+"_"+instruments_name)

        file_db.filename = filename
        file_db.format = mimetype

        db.session.add(file_db)
        db.session.commit()

        file.save(os.path.join(current_app.config["FILES"]["DIR"], get_full_filename(filename, mimetype)))
        return file_db

    def put(self, args):
        pass

    def patch(self, args):
        pass

    @file_blp.response(code=204)
    def delete(self, args):
        pass

@file_blp.route("/<id>", endpoint="byid")
class FilesApiById(MethodView):
    
    @file_blp.response(code=200)
    def get(self, id):
        file = Files.query.filter_by(id=id).first()
        try:
            return send_from_directory(
                os.path.join(os.getcwd(), current_app.config["FILES"]["DIR"]),
                get_full_filename(file.filename, file.format))
        except FileNotFoundError:
            return abort(404, message="File not found")

    @file_blp.arguments(FileUploadSchema, location="files")
    def post(self, args, id):
        # TODO: Implement it to make it able to update files of an existed id
        pass

    def put(self, args, id):
        pass

    def patch(self, args, id):
        pass

    @file_blp.response(code=204)
    def delete(self, id):
        file = Files.query.filter_by(id=id).first()
        db.session.delete(file)
        os.remove(os.path.join(current_app.config["FILES"]["DIR"],
            get_full_filename(file.filename, file.format)))
        db.session.commit()
        return None