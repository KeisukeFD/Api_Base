from datetime import datetime, timedelta
from flask import Blueprint, request

bp = Blueprint('default', __name__)

from app import schema
from models.schemas.admin.login import login_schema
from services.authentication import AuthService
from services.sessions import SessionService
from utils import functions, shortcuts
from utils.decorators import required_authorization, logging
from services.loggers import LoggerService


@bp.route('/')
@logging
def home():
    return ''


@bp.route('/login', methods=['POST'])
@schema.validate(login_schema)
@logging
def login():
    data = request.get_json()
    try:
        someone = AuthService.instance().login(data['username'], data['password'])
        now = datetime.utcnow()
        expiration = now + timedelta(minutes=5)
        payload = {
            'exp': expiration,
            'iat': now,
            'sub': someone.id,
            'username': someone.username
        }
        token = functions.get_token(payload)

        active_session = SessionService.instance().get(someone.id)
        if active_session and active_session.expiration > now:
            token = active_session.token
        elif active_session:
            SessionService.instance().delete(someone.id)
            SessionService.instance().set(someone.id, token, expiration)
        else:
            SessionService.instance().set(someone.id, token, expiration)

        return shortcuts.success('Welcome inside !', token=token)
    except Exception as e:
        LoggerService.instance().debug(e)
        return shortcuts.error('Invalid login !'), 401


@bp.route('/logout', methods=['POST'])
@required_authorization
def logout(payload):
    SessionService.instance().delete(payload['sub'])
    return shortcuts.error('Logged out !')

