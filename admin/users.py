from flask import Blueprint, request

bp = Blueprint('admin-users', __name__)

from app import db, schema
from utils import shortcuts
from utils.decorators import required_authorization, required_role
from model import User, UserSchema, Role, RoleSchema
from models.schemas.admin.user import new_user_schema, edit_user_schema, user_roles_schema

DEFAULT_ADMIN_ROLE = "Admin"


# ******** Private functions ******** #
def _get_roles(input_roles):
    """
    Get the list of 'roles' from request.data pass in param 'input_roles'
    and return the list of type role if it match.

    :exception The number of roles doesn't match between the list and the database request.
    :param input_roles: [integer]
    :return: [Role] or None
    """
    if 'roles' in input_roles and isinstance(input_roles['roles'], list):
        roles = Role.query.filter(Role.id.in_(input_roles['roles'])).all()
        if len(roles) != len(input_roles['roles']):
            db_roles = [r.id for r in roles]
            not_roles = [str(r) for r in input_roles['roles'] if r not in db_roles]
            raise Exception(["Roles '%s' is not available" % r for r in not_roles])
        return roles
    return None


# ******** Public Routes ******** #
@bp.route('/', methods=['GET'])
@required_authorization
@required_role([DEFAULT_ADMIN_ROLE])
def get_all_users(payload):
    users = User.query.all()
    if users:
        users = UserSchema(many=True).dump(users)
        return shortcuts.success(None, users=users.data)
    return shortcuts.error('Not found !'), 404


@bp.route('/<int:user_id>', methods=['GET'])
@required_authorization
@required_role([DEFAULT_ADMIN_ROLE])
def get_user(payload, user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return shortcuts.success('', user=UserSchema().dump(user))
    return shortcuts.error('Not found !'), 404


@bp.route('/roles', methods=['GET'])
@required_authorization
@required_role([DEFAULT_ADMIN_ROLE])
def get_roles(payload):
    roles = Role.query.all()
    if roles:
        roles = RoleSchema(many=True).dump(roles)
        return shortcuts.success(None, roles=roles)
    return shortcuts.error('Not found !'), 404


@bp.route('/<int:user_id>', methods=['PUT'])
@required_authorization
@required_role([DEFAULT_ADMIN_ROLE])
@schema.validate(edit_user_schema)
def edit_user(payload, user_id):
    try:
        data = request.get_json()
        if not data:
            return shortcuts.success('Nothing to do !')
        user = User.query.filter_by(id=user_id).first()
        msgs = []
        if 'username' in data and user.username != data['username']:
            user.username = data['username']
            msgs.append("Username has been changed")
        if 'password' in data:
            user.set_password(data['password'])
            msgs.append("Password has been changed")
        if 'email' in data and user.email != data['email']:
            user.email = data['email']
            msgs.append("Email has been changed")

        if msgs:
            db.session.add(user)
            db.session.commit()
            return shortcuts.success(msgs)

        return shortcuts.success("Nothing's changed !")
    except Exception as e:
        return shortcuts.error(e.args)


@bp.route('/<int:user_id>', methods=['DELETE'])
@required_authorization
@required_role([DEFAULT_ADMIN_ROLE])
def delete_user(payload, user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return shortcuts.success('User has been successfully deleted !')
    except Exception as e:
        return shortcuts.error(e.args)
    return shortcuts.success("Nothing's to do !")


@bp.route('/', methods=['POST'])
@required_authorization
@required_role([DEFAULT_ADMIN_ROLE])
@schema.validate(new_user_schema)
def add_user(payload):
    if not request.get_json():
        return shortcuts.error('Malformed request'), 400
    try:
        data = request.get_json()
        new_user = User(data['username'], data['email'], data['password'])

        roles = _get_roles(data)
        for role in roles:
            new_user.roles.append(role)

        db.session.add(new_user)
        db.session.commit()

        return shortcuts.success('User has been successfully added !', new_user=new_user.id)
    except Exception as e:
        return shortcuts.error(e.args[0])


@bp.route('/<int:user_id>/roles', methods=['PUT'])
@required_authorization
@required_role([DEFAULT_ADMIN_ROLE])
@schema.validate(user_roles_schema)
def set_user_roles(payload, user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            roles = _get_roles(request.get_json())
            user.roles = roles

            db.session.add(user)
            db.session.commit()
            return shortcuts.success('Roles for user {} has been successfully modified !'.format(user_id))
        return shortcuts.success("Nothing's changed !")
    except Exception as e:
        return shortcuts.error(e.args)
