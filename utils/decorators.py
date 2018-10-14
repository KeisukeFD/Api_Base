from functools import wraps
from flask import request
from services.sessions import SessionService
from .functions import verify_token
from .shortcuts import error
from services.authentication import AuthService
from app import config
from services.loggers import LoggerService


def logging(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        LoggerService.instance().log(info="Entering %s()" % f.__name__, debug=args)
        return f(*args, **kwargs)
    return decorated_func


def required_authorization(f):
    """
    Required authorization, check the request header to identify the Authorization Bearer
     Extract and verify the token
    :return: payload: dict
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth = request.headers['Authorization'].split()
            LoggerService.instance().log(info="Trying to validate authorization access.")
            if auth[0] == 'Bearer':
                LoggerService.instance().debug("Verifying token")
                payload = verify_token(auth[1])
                LoggerService.instance().debug("Getting active session for 'user_id=%s'" % payload['sub'])
                SessionService.instance().get(payload['sub'], exception=True)
                LoggerService.instance().info("Authorized with success")
                return f(payload, *args, **kwargs)
        except Exception as e:
            LoggerService.instance().error("".join(e.args))
            return error(['You must login first: ', '%slogin' % config['BASE_URL']]), 401
    return decorated_function


def required_role(roles):
    """
    Required role check if the user logged have the correct role to continue
    :param roles: list
    """
    def decorated_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user_id = args[0]['sub']
                user_roles = AuthService.instance().get_user_roles(user_id)
                LoggerService.instance().log(info="Checking roles",
                                             debug="roles [%s] for 'user_id=%s'" % (",".join([r.name for r in user_roles]), user_id))
                for user_role in user_roles:
                    if user_role.name.upper() in [r.upper() for r in roles]:
                        return f(*args, **kwargs)
            except Exception as _:
                pass
            return error(['Forbidden: One of these roles are required', roles]), 403
        return wrapper
    return decorated_func
