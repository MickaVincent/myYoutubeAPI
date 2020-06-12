from api.utils.database import db
from sqlalchemy.orm import validates
from api.models.user import User
import datetime
import re
import secrets


class Token(db.Model):
    __tablename__ = "tokens"

    id = db.Column('id', db.Integer, autoincrement=True, nullable=False, primary_key=True)
    code = db.Column('code', db.VARCHAR(45), nullable=False, index=True, unique=True)
    expired_at = db.Column('expired_at', db.DateTime, nullable=False)
    user_uuid = db.Column('user_uuid', db.VARCHAR(36),
                                       db.ForeignKey(name="fk_token_user1",
                                                  column="users.uuid",
                                                  onupdate='NO ACTION',
                                                  ondelete='SET NULL'),
                                                  nullable=True)

    def __init__(self, user_uuid):
        self.generate_token()
        self.user_uuid = user_uuid

    def generate_token(self):
        expired_at = datetime.datetime.now() + datetime.timedelta(days=30)
        expired_at.strftime("%Y-%m-%d %H:%M:%S")
        self.code = secrets.token_hex(22)
        self.expired_at = expired_at
        return dict(code=self.code, expired_at=self.expired_at)

    def check_validity(self):
        date_token = self.expired_at.strftime("%Y-%m-%d %H:%M:%S")
        today_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return not date_token < today_date

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

    def get_code(self):
        return self.code

    def get_expired_at(self):
        return self.expired_at

    def get_user_uuid(self):
        return self.user_uuid

    def get_as_dict(self):
        return dict(
            token=self.code,
            user=(db.session.query(User).filter_by(uuid=self.user_uuid).first()).get_as_dict(True)
        )

    @validates('id')
    def check_id(self, key, value):
        assert isinstance(value, int) is True, "id is invalid"
        return value

    @validates('code')
    def check_code(self, key, value):
        return value

    @validates('expired_at')
    def check_expired_at(self, key, value):
        test = str(value)
        regex = re.compile(
            """^(\d\d\d\d)-((0\d)|(1[012]))-(([012]\d)|(3[01])).(([01]\d)|(2[0123])):([0-5]\d)(:([0-5]\d)(\.\d+)?)?([zZ]|[\+\-]\d\d:\d\d)?$""")
        assert re.match(regex, test) is not None, "time format is invalid"
        return value

    @validates('user_uuid')
    def check_user_uuid(self, key, value):
        uuid_regex = re.compile("""^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$""")
        assert re.match(uuid_regex, value) is not None, "user_uuid is not valid"
        return value
