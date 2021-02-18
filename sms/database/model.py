from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# TODO: Encapsulate models into a class

# Model part
# Middle tables
# Groups & Pieces
groups_pieces = db.Table('groupsPieces',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True, nullable=False),
    db.Column('piece_id', db.Integer, db.ForeignKey('pieces.id'), primary_key=True, nullable=False)
)

# Instruments & Pieces
instruments_pieces = db.Table('instrumentsPieces',
    db.Column('instrument_ID', db.Integer, db.ForeignKey('instruments.id'), primary_key=True, nullable=False),
    db.Column('piece_ID', db.Integer, db.ForeignKey('pieces.id'), primary_key=True, nullable=False)
)

# Instruments & Files
instruments_files = db.Table('instrumentsFiles',
    db.Column('instrument_ID', db.Integer, db.ForeignKey('instruments.id'), primary_key=True, nullable=False),
    db.Column('file_ID', db.Integer, db.ForeignKey('files.id'), primary_key=True, nullable=False)
)

# Pieces & Files
pieces_files = db.Table("piecesFiles",
    db.Column('piece_id', db.Integer, db.ForeignKey('pieces.id'), primary_key=True, nullable=False),
    db.Column('file_id', db.Integer, db.ForeignKey('files.id'), primary_key=True, nullable=False)
)

# Tables
class Groups(db.Model):
    __tablename__ = "groups"
    # Columns
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    # Relationships
    parts = db.relationship("Parts", backref="group", lazy=True)
    pieces = db.relationship("Pieces", secondary=groups_pieces, lazy="subquery", backref=db.backref("groups", lazy=True))
    
    def __repr__(self) -> str:
        return str({
            "Table": "groups",
            "id": self.id,
            "name": self.name
        })

class Parts(db.Model):
    __tablename__ = "parts"
    # Columns
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    # Foreign Keys
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    # Relationships
    instruments = db.relationship("Instruments", backref="part", lazy=True)
    
    def __repr__(self) -> str:
        return str({
            "Table": "parts",
            "id": self.id,
            "name": self.name
        })
        
class Instruments(db.Model):
    __tablename__ = "instruments"
    # Columns
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    # Foreign Keys
    part_id = db.Column(db.Integer, db.ForeignKey("parts.id"), nullable=False)
    # Relationships
    pieces = db.relationship('Pieces', secondary=instruments_pieces, lazy='subquery', backref=db.backref('instruments', lazy=True))
    files = db.relationship('Files', secondary=instruments_files, lazy='subquery', backref=db.backref('instruments', lazy=True))

    def __repr__(self) -> str:
        return str({
            "Table": "instruments",
            "id": self.id,
            "name": self.name
        })

class Pieces(db.Model):
    __tablename__ = "pieces"
    # Columns
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text)
    lyricist = db.Column(db.Text)
    arranger = db.Column(db.Text)
    opus = db.Column(db.Integer)
    copyright_expire_date = db.Column(db.Date)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now())
    modified_time = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    # Relationships
    # groups_pieces many-to-many
    # instruments_pieces many-to-many
    files = db.relationship('Files', backref="piece", lazy=True)
    transposes = db.relationship("Transposes", backref="pieces", lazy=True)

    def onModified(self):
        self.modified_time = datetime.datetime.now()

    def __repr__(self) -> str:
        return str({
            "Table": "pieces",
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "lyricist": self.lyricist,
            "arranger": self.arranger,
            "opus": self.opus,
            "copyright_expire_date": self.copyright_expire_date,
            "created_time": self.created_time,
            "modified_time": self.modified_time
        })

class Transposes(db.Model):
    __tablename__ = "transposes"
    # Columns
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    from_bar = db.Column(db.Integer)
    to_bar = db.Column(db.Integer)
    # Foreign Keys
    from_instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.id'), nullable=False)
    to_instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.id'), nullable=False)
    piece_id = db.Column(db.Integer, db.ForeignKey('pieces.id'), nullable=False)
    # Relationships
    from_instrument = db.relationship("Instruments", foreign_keys=[from_instrument_id])
    to_instrument = db.relationship("Instruments", foreign_keys=[to_instrument_id])

    def __repr__(self) -> str:
        return str({
            "Table": "transposes",
            "id": self.id
        })

class Files(db.Model):
    __tablename__ = "files"
    # Columns
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    created_time = db.Column(db.DateTime, default=datetime.datetime.now())
    format = db.Column(db.Text)
    filename = db.Column(db.Text)
    # Foreign Keys
    piece_id = db.Column(db.Integer, db.ForeignKey('pieces.id'), nullable=False)
    # Relationships
    # instruments_files many-to-many

    def __repr__(self) -> str:
        return str({
            "Table": "files",
            "id": self.id,
            "created_time": self.created_time,
            "format": self.format,
            "filename": self.filename
        })