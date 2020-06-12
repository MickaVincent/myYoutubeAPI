from api.utils.database import db
from sqlalchemy.orm import validates
import datetime
import re


class VideoFormat(db.Model):
    __tablename__ = "video_formats"

    id = db.Column('id', db.Integer, autoincrement=True, nullable=False, primary_key=True)
    code = db.Column('code', db.VARCHAR(45), nullable=False)
    uri = db.Column('uri', db.VARCHAR(512), nullable=False)
    video_uuid = db.Column('video_uuid', db.VARCHAR(36),
                           db.ForeignKey(name="fk_video_uuid",
                                         column="videos.uuid",
                                         onupdate='NO ACTION',
                                         ondelete='NO ACTION'),
                           nullable=True, index=True)

    def __init__(self, code, uri, video_uuid):
        self.code = code
        self.uri = uri
        self.video_uuid = video_uuid

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def get_as_dict(self):
        return {self.code: self.uri}

    @validates('id')
    def check_id(self, key, value):
        assert isinstance(value, int) is True, "id is invalid"
        return value

    @validates('code')
    def check_code(self, key, value):
        return value

    @validates('uri')
    def check_uri(self, key, value):
        return value

    @validates('video_uuid')
    def check_video_uuid(self, key, value):
        uuid_regex = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$")
        assert re.match(uuid_regex, value) is not None, "video_uuid is not valid"
        return value
