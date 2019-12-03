from config import db, ma


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filename = db.Column(db.String(), index=True)
    sha1 = db.Column(db.String(), unique=True)
    md5 = db.Column(db.String())
    file_type = db.Column(db.String())
    file_size = db.Column(db.Integer)


class FileSchema(ma.ModelSchema):
    class Meta:
        model = File
        sqla_session = db.session
