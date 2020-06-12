from api.utils.database import db
from sqlalchemy.orm import validates
from api.models.user import User
import re
from html import escape


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column('id', db.Integer, autoincrement=True, nullable=False, primary_key=True)
    body = db.Column('body', db.TEXT, nullable=False)
    user_uuid = db.Column('user_uuid', db.VARCHAR(36),
                                       db.ForeignKey(name="fk_comment_user1",
                                                     column="users.uuid",
                                                     onupdate='NO ACTION',
                                                     ondelete='NO ACTION'),
                                                     nullable=False)
    video_id = db.Column('video_uuid', db.VARCHAR(36),
                                     db.ForeignKey(name="fk_comment_video1",
                                                   column="videos.uuid",
                                                   onupdate='NO ACTION',
                                                   ondelete='NO ACTION'),
                                                   nullable=False)

    def __init__(self, body, user_uuid, video_id):
        self.body = body
        self.user_uuid = user_uuid
        self.video_id = video_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def get_id(self):
        return self.id

    def get_body(self):
        return self.body

    def get_user_uuid(self):
        return self.user_uuid

    def get_video_uuid(self):
        return self.video_uuid

    def get_as_dict(self):
        return dict(
            id=self.id,
            body=self.body,
            user=(db.session.query(User).filter_by(uuid=self.user_uuid).first()).get_as_dict()
        )

    @validates('id')
    def check_id(self, key, value):
        assert isinstance(value, int) is True, "id is invalid"
        return value

    # @validates('body')
    # def check_body(self, key, value):
    #     value = escape(value)
    #     regex = re.compile("""(/)|(\|)|({)|(})|(`)|(\\)""")
    #     assert re.search(regex, value)
    #     return value

    @validates('user_uuid')
    def check_user_uuid(self, key, value):
        uuid_regex = re.compile("""^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$""")
        assert re.match(uuid_regex, value) is not None, "user_uuid is not valid"
        return value

    @validates('video_uuid')
    def check_video_uuid(self, key, value):
        uuid_regex = re.compile("""^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$""")
        assert re.match(uuid_regex, value) is not None, "video_uuid is not valid"
        return value
