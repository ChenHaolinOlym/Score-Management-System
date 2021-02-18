from flask_smorest import Api

from .baseSchema import ma
from .groups import group_blp
from .parts import part_blp
from .instruments import instrument_blp
from .pieces import piece_blp
from .transposes import transpose_blp
from .files import file_blp

api = Api()

def register_bluprints():
    api.register_blueprint(group_blp)
    api.register_blueprint(part_blp)
    api.register_blueprint(instrument_blp)
    api.register_blueprint(piece_blp)
    api.register_blueprint(transpose_blp)
    api.register_blueprint(file_blp)