from app import db
from models.admin.User import Session
from utils.functions import Struct
from singleton.singleton import Singleton


@Singleton
class SessionService:
    @staticmethod
    def set(user_id, token, expiration):
        new_session = Session(user_id, token, expiration)
        db.session.add(new_session)
        db.session.commit()

    @staticmethod
    def get(user_id, exception=False):
        active_session = Session.query.filter_by(user_id=user_id).first()
        if active_session:
            result = {
                'user_id': active_session.user_id,
                'token': active_session.token,
                'expiration': active_session.expiration
            }
            return Struct(result)
        if exception:
            raise Exception('No session found !')
        return None

    @staticmethod
    def delete(user_id):
        Session.query.filter_by(user_id=user_id).delete()
        db.session.commit()
