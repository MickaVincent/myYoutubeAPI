from api.utils.database import db
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash
import datetime
import uuid
import re


class User(db.Model):
    __tablename__ = "users"

    uuid = db.Column(db.VARCHAR(36), primary_key=True, nullable=False)
    username = db.Column(db.VARCHAR(45), unique=True, nullable=False)
    email = db.Column(db.VARCHAR(255), unique=True, nullable=False)
    pseudo = db.Column(db.VARCHAR(45), nullable=True)
    password = db.Column(db.VARCHAR(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password, pseudo):
        self.uuid = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.pseudo = pseudo
        self.password = generate_password_hash(password, method='sha256')
        self.created_at = datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_username(self, username):
        self.username = username
        db.session.commit()
        return self

    def update_pseudo(self, pseudo):
        self.pseudo = pseudo
        db.session.commit()
        return self

    def update_email(self, email):
        self.email = email
        db.session.commit()
        return self

    def update_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
        db.session.commit()
        return self

    def get_as_dict(self, isOwner=False):
        user = {}
        user['uuid'] = self.uuid
        user['username'] = self.username
        user['pseudo'] = self.pseudo
        user['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if isOwner:
            user['email'] = self.email
        return user

    @validates('uuid')
    def check_uuid(self, key, value):
        uuid_regex = re.compile("""^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$""")
        assert re.match(uuid_regex, value) is not None, "uuid is not valid"
        return value

    @validates('username')
    def check_username(self, key, value):
        username_regex = re.compile("""^[(a-z)(A-Z)(0-9)(\-\_)]{1,45}$""")
        assert re.match(username_regex, value) is not None, 'Username is invalid, must be betweed 5 and 45 alphanumeric characters.'
        return value

    @validates('email')
    def check_email(self, key, value):
        email_regex = re.compile("""^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$""")
        assert re.match(email_regex, value.casefold()) is not None, 'Email is invalid.'
        return value.casefold()

    @validates('pseudo')
    def check_pseudo(self, key, value):
        pseudo_regex = re.compile("""^[(a-z)(A-Z)(0-9)(\-\_)]{0,45}$""")
        assert re.match(pseudo_regex, value) is not None, 'Pseudo is invalid, must be betweed 5 and 45 alphanumeric characters.'
        return value

    @validates('password')
    def check_password(self, key, value):
        password_regex = re.compile("""^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$""")
        assert re.match(password_regex, value) is not None, 'Password format is invalid, must have at least letter, one number and one special character.'
        return value
