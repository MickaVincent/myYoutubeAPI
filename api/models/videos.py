from api.utils.database import db
from api.models.user import User
from sqlalchemy.orm import validates
from uuid import uuid4
from api.models.videoformat import VideoFormat
import datetime
import re


class Video(db.Model):
    __tablename__ = "videos"

    uuid = db.Column('uuid', db.VARCHAR(36), primary_key=True, index=True, nullable=False)
    name = db.Column('name', db.VARCHAR(45), nullable=True)
    duration = db.Column('duration', db.Integer, nullable=False)
    user_uuid = db.Column('user_uuid', db.VARCHAR(36), db.ForeignKey(name="fk_video_user",
                                                                     column="users.uuid",
                                                                     onupdate='NO ACTION',
                                                                     ondelete='NO ACTION'))
    source = db.Column('source', db.VARCHAR(512), nullable=False)
    created_at = db.Column('created_at', db.DateTime, nullable=False)
    views = db.Column('views', db.Integer, nullable=False)
    enabled = db.Column('enabled', db.Boolean, nullable=False)

    def __init__(self, name, duration, user_uuid, source, enabled):
        self.uuid = str(uuid4())
        self.name = name
        self.duration = duration
        self.user_uuid = user_uuid
        self.source = source
        self.created_at = datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.views = 0
        self.enabled = enabled

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update_name(self, name):
        self.name = name
        db.session.commit()
        return self

    def update_user(self, user):
        self.user_uuid = user
        db.session.commit()
        return self

    def get_as_dict(self):
        format_list = []
        formats = db.session.query(VideoFormat).filter_by(video_uuid=self.uuid).all()
        for format in formats:
            format_list = format.get_as_dict()

        video = dict(
            id=self.uuid,
            name=self.name,
            user=(db.session.query(User).filter_by(uuid=self.user_uuid).first()).get_as_dict(),
            source=self.source,
            created_at=self.created_at.strftime(("%Y-%m-%d %H:%M:%S")),
            views=self.views,
            enabled=self.enabled,
            format=format_list
        )
        return video

    @validates('uuid')
    def check_id(self, key, value):
        uuid_regex = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$")
        assert re.match(uuid_regex, value) is not None, "video_uuid is not valid"
        return value

    @validates('name')
    def check_name(self, key, value):
        regex = re.compile("""^[\w!.?;,\/\-\_\%\*\#\é\è\=\-\&\s]{1,45}$""")
        assert re.match(regex, value) is not None, "video name is invalid"
        return value

    @validates('duration')
    def check_duration(self, key, value):
        assert isinstance(value, int) is True, "duration is invalid"
        return value

    @validates('user_uuid')
    def check_uuid(self, key, value):
        uuid_regex = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$")
        assert re.match(uuid_regex, value) is not None, "user_uuid is not valid"
        return value

    @validates('source')
    def check_source(self, key, value):
        # A vérifier en fonction du type de source généré par le code de flo
        # regex = re.compile("^[(a-z)(A-Z)(0-9)]{5,45}$")
        # assert re.match(regex, value) is not None, "source is invalid"
        return value

    @validates('created_at')
    def check_created_at(self, key, value):
        regex = re.compile("""^(\d\d\d\d)-((0\d)|(1[012]))-(([012]\d)|(3[01])).(([01]\d)|(2[0123])):([0-5]\d)(:([0-5]\d)(\.\d+)?)?([zZ]|[\+\-]\d\d:\d\d)?$""")
        assert re.match(regex, str(value)) is not None, "time format is invalid"
        return value

    @validates('views')
    def check_views(self, key, value):
        assert isinstance(value, int) is True, "views is invalid"
        return value

    @validates('enabled')
    def check_enabled(self, key, value):
        assert isinstance(value, bool) is True, "enabled is invalid"
        return value
