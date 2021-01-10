from passlib.hash import bcrypt_sha256
from string import ascii_letters
from app import db, marshmallow, config
from marshmallow import fields
from models.utils.Mixins import TimestampMixin

user_role = db.Table('user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(800), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    reset_token = db.Column(db.String(800))
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('users', lazy=True), lazy='subquery')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def _get_salt(self):
        secret = [c for c in config['SECRET_KEY'] if c in ascii_letters]
        return ''.join(secret)[:22].ljust(22, '9')

    def set_password(self, plain_password):
        self.password = bcrypt_sha256.using(salt=self._get_salt()).hash(plain_password)

    def verify_password(self, password):
        if not bcrypt_sha256.using(salt=self._get_salt()).verify(password, self.password):
            raise Exception('Invalid password !')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Session(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    token = db.Column(db.String(800), nullable=False, unique=True)
    expiration = db.Column(db.DateTime)

    def __init__(self, user_id, token, expiration):
        self.user_id = user_id
        self.token = token
        self.expiration = expiration


# ******** JSON Serialization Schemas ******** #
class RoleSchema(marshmallow.Schema):
    class Meta:
        model = Role
        fields = ('id', 'name')


class UserSchema(marshmallow.Schema):
    roles = fields.Nested(RoleSchema, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'roles')

