import logging
import os
from flask import jsonify
from flask import current_app
from flask import send_file, Response
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .extend import ApiGeneralException
from ..database import db
from ..database import (
    Groups,
    Parts,
    Instruments,
    Pieces,
    Versions,
    Transposes,
    Files,
)
from .schema import (
    GroupSchema,
    GroupBaseSchema,
    PartSchema,
    PartBaseSchema,
    InstrumentSchema,
    InstrumentBaseSchema,
    PieceSchema,
    PieceBaseSchema,
    VersionSchema,
    VersionBaseSchema,
    TransposeSchema,
    TransposeBaseSchema,
    FileSchema,
    FileBaseSchema
)

# logger init
logger = logging.getLogger(__name__)

# result wrapper
def result_wrapper(data:dict={}, status:bool=True, code:int=200, message:str="0") -> dict:
    return {
        "success": status,
        "code": code,
        "data": data,
        "message": message
    }

class GroupsApi(Resource):
    def get(self) -> str:
        groups = Groups.query.all()
        return jsonify(result_wrapper(GroupBaseSchema(many=True).dump(groups)))

    def post(self) -> None:
        raise ApiGeneralException("post operation on groups is forbidden", 403)
    def put(self) -> None:
        raise ApiGeneralException("put operation on groups is forbidden", 403)
    def patch(self) -> None:
        raise ApiGeneralException("patch operation on groups is forbidden", 403)
    def delete(self) -> None:   
        raise ApiGeneralException("delete operation on groups is forbidden", 403)

class GroupApi(Resource):
    def get(self, id:int) -> str:
        group = Groups.query.filter_by(id=id).first()
        return jsonify(result_wrapper(GroupSchema().dump(group)))

    def post(self, id:int) -> None:
        raise ApiGeneralException("post operation is forbidden", 403)
    def put(self, id:int) -> None:
        raise ApiGeneralException("put operation on group is forbidden", 403)
    def patch(self, id:int) -> None:
        raise ApiGeneralException("patch operation on group is forbidden", 403)
    def delete(self, id:int) -> None:
        raise ApiGeneralException("delete operation on group is forbidden", 403)

class PartsApi(Resource):
    def get(self) -> str:
        parts = Parts.query.all()
        return jsonify(result_wrapper(PartBaseSchema(many=True).dump(parts)))

    def post(self) -> None:
        raise ApiGeneralException("post operation on parts is forbidden", 403)
    def put(self) -> None:
        raise ApiGeneralException("put operation on parts is forbidden", 403)
    def patch(self) -> None:
        raise ApiGeneralException("patch operation on parts is forbidden", 403)
    def delete(self) -> None:
        raise ApiGeneralException("delete operation on parts is forbidden", 403)

class PartApi(Resource):
    def get(self, id) -> str:
        part = Parts.query.filter_by(id=id).first()
        return jsonify(result_wrapper(PartSchema().dump(part)))

    def post(self, id:int) -> None:
        raise ApiGeneralException("post operation is forbidden", 403)
    def put(self, id:int) -> None:
        raise ApiGeneralException("put operation on part is forbidden", 403)
    def patch(self, id:int) -> None:
        raise ApiGeneralException("patch operation on part is forbidden", 403)
    def delete(self, id:int) -> None:
        raise ApiGeneralException("delete operation on part is forbidden", 403)

class InstrumentsApi(Resource):
    def get(self) -> str:
        instruments = Instruments.query.all()
        return jsonify(result_wrapper(InstrumentBaseSchema(many=True).dump(instruments)))

    def post(self) -> None:
        raise ApiGeneralException("post operation on instruments is forbidden", 403)
    def put(self) -> None:
        raise ApiGeneralException("put operation on instruments is forbidden", 403)
    def patch(self) -> None:
        raise ApiGeneralException("patch operation on instruments is forbidden", 403)
    def delete(self) -> None:
        raise ApiGeneralException("delete operation on instruments is forbidden", 403)

class InstrumentApi(Resource):
    def get(self, id:int) -> str:
        instrument = Instruments.query.filter_by(id=id).first()
        return jsonify(result_wrapper(InstrumentBaseSchema().dump(instrument)))

    def post(self, id:int) -> None:
        raise ApiGeneralException("post operation is forbidden", 403)
    def put(self, id:int) -> None:
        raise ApiGeneralException("put operation on instrument is forbidden", 403)
    def patch(self, id:int) -> None:
        raise ApiGeneralException("patch operation on instrument is forbidden", 403)
    def delete(self, id:int) -> None:
        raise ApiGeneralException("delete operation on instrument is forbidden", 403)

class PiecesApi(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", type=str, required=True)
        self.parser.add_argument("author", type=str)
        self.parser.add_argument("lyricist", type=str)
        self.parser.add_argument("arranger", type=str)
        self.parser.add_argument("opus", type=int)
        # self.parser.add_argument("copyright_expire_date", type=str)

    def get(self) -> str:
        pieces = Pieces.query.all()
        return jsonify(result_wrapper(PieceSchema(many=True).dump(pieces)))

    def post(self) -> str:
        args = self.parser.parse_args()
        piece = Pieces(**args)
        db.session.add(piece)
        db.session.commit()
        logger.info(f"Add Pieces to database. Data: {piece}")
        return result_wrapper(code=201), 201

    def put(self) -> str:
        pass

    def patch(self) -> str:
        pass

    def delete(self) -> str:
        pass

class PieceApi(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", type=str, required=True)
        self.parser.add_argument("author", type=str)
        self.parser.add_argument("lyricist", type=str)
        self.parser.add_argument("arranger", type=str)
        self.parser.add_argument("opus", type=int)
        self.parser.add_argument("copyright_expire_date", type=str)

    def get(self, id:int) -> str:
        piece = Pieces.query.filter_by(id=id).first()
        return jsonify(result_wrapper(PieceSchema().dump(piece)))

    def post(self, id:int) -> str:
        raise ApiGeneralException("post operation on singular resource is forbidden", 403)

    def put(self, id:int) -> str:
        pass

    def patch(self, id:int) -> str:
        pass

    def delete(self, id:int) -> str:
        pass

class VersionsApi(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()

    def get(self) -> str:
        versions = Versions.query.all()
        return jsonify(result_wrapper(VersionSchema(many=True).dump(versions)))

    def post(self) -> str:
        pass

    def put(self) -> str:
        pass

    def patch(self) -> str:
        pass

    def delete(self) -> str:
        pass

class VersionApi(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()

    def get(self, id:int) -> str:
        version = Versions.query.filter_by(id=id).first()
        return jsonify(result_wrapper(VersionSchema().dump(version)))

    def post(self, id:int) -> str:
        pass

    def put(self, id:int) -> str:
        pass

    def patch(self, id:int) -> str:
        pass

    def delete(self, id:int) -> str:
        pass

class TransposesApi(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()

    def get(self) -> str:
        transposes = Transposes.query.all()
        return jsonify(result_wrapper(TransposeSchema(many=True).dump(transposes)))

    def post(self) -> str:
        pass

    def put(self) -> str:
        pass

    def patch(self) -> str:
        pass

    def delete(self) -> str:
        pass

class TransposeApi(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()

    def get(self, id:int) -> str:
        transpose = Transposes.query.filter_by(id=id).first()
        return jsonify(result_wrapper(TransposeSchema().dump(transpose)))

    def post(self, id:int) -> str:
        pass

    def put(self, id:int) -> str:
        pass

    def patch(self, id:int) -> str:
        pass

    def delete(self, id:int) -> str:
        pass

class FilesApi(Resource):
    def get(self) -> str:
        files = Files.query.all()
        return jsonify(result_wrapper(FileSchema(many=True).dump(files)))

    def post(self) -> str:
        parser = reqparse.RequestParser()
        parser.add_argument("file_type", type=int)
        parser.add_argument("file", type=FileStorage, location="files")
        args = parser.parse_args()
        file = args["file"]
        if file.filename == "":
            raise ApiGeneralException("No file is posted", 400)
        if file:
            # filename = secure_filename(file.filename)
            mimetype = file.content_type.split("/")[1]
            myfile = Files(format=mimetype, file_type=args["file_type"])
            db.session.add(myfile)
            db.session.flush()
            id = myfile.id
            file.save(os.path.join(current_app.config["FILES"]["DIR"], "\\"+str(id)+"."+mimetype))
            db.session.commit()

    def delete(self) -> str:
        pass

class FileApi(Resource):
    def get(self, id:int) -> str:
        file = Files.query.filter_by(id=id).first()
        return jsonify(result_wrapper(FileSchema().dump(file)))

    def post(self, id:int) -> str:
        raise ApiGeneralException("post operation on singular resource is forbidden", 403)

    def delete(self, id:int) -> str:
        pass
        # parser = self.parser.copy()
        # parser.add_argument("id", type=int)
        # args = parser.parse_args()
        # # TODO: Complete Delete process

class DownloadApi(Resource):
    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()

    def get(self, id:int) -> Response:
        file = Files.query.filter_by(id=id).first()
        return send_file(os.path.join(current_app.config["FILES"]["DIR"], "\\"+str(id)+"."+file.format))