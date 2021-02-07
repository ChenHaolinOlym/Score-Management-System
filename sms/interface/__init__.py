from werkzeug.exceptions import HTTPException

from .extend import Api, ApiGeneralException
from .schema import ma
from .restful import (
    GroupsApi,
    GroupApi,
    PartsApi,
    PartApi,
    InstrumentsApi,
    InstrumentApi,
    PiecesApi,
    PieceApi,
    VersionsApi,
    VersionApi,
    TransposesApi,
    TransposeApi,
    FilesApi,
    FileApi,
    DownloadApi
)

api = Api()

# add resources
api.add_resource(GroupsApi, "/api/groups", endpoint="groups_api")
api.add_resource(GroupApi, "/api/group/<id>", endpoint="group_api")

api.add_resource(PartsApi, "/api/parts", endpoint="parts_api")
api.add_resource(PartApi, "/api/part/<id>", endpoint="part_api")

api.add_resource(InstrumentsApi, "/api/instruments", endpoint="instruments_api")
api.add_resource(InstrumentApi, "/api/instrument/<id>", endpoint="instrument_api")

api.add_resource(PiecesApi, "/api/pieces", endpoint="pieces_api")
api.add_resource(PieceApi, "/api/piece/<id>", endpoint="piece_api")

api.add_resource(VersionsApi, "/api/versions", endpoint="versions_api")
api.add_resource(VersionApi, "/api/version/<id>", endpoint="version_api")

api.add_resource(TransposesApi, "/api/transposes", endpoint="transposes_api")
api.add_resource(TransposeApi, "/api/transpose/<id>", endpoint="transpose_api")

api.add_resource(FilesApi, "/api/files", endpoint="files_api")
api.add_resource(FileApi, "/api/file/<id>", endpoint="file_api")

api.add_resource(DownloadApi, "/download/<id>")