from models.admin.User import User
from singleton.singleton import Singleton


@Singleton
class AuthService:

    @staticmethod
    def login(username, password):
        someone = User.query.filter_by(username=username).first()
        someone.verify_password(password)
        return someone

    @staticmethod
    def user_has_role(user_id, role_name):
        user = User.query.filter_by(id=user_id).first()
        for role in user.roles:
            if role.name.upper() == role_name.upper():
                return True
        return False

    @staticmethod
    def get_user_roles(user_id):
        user = User.query.filter_by(id=user_id).first()
        return user.roles
