import jwt
from flask_sqlalchemy import get_debug_queries
from app import config
from services.loggers import LoggerService


# **** Session Token Management **** #
def get_token(payload):
    return jwt.encode(payload, config['SECRET_KEY'], algorithm='HS256')


def verify_token(token):
    return jwt.decode(token, config['SECRET_KEY'], algorithms=['HS256'])


# **** Struct to convert Dict to Object (Dot Notation) **** #
class Struct(object):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __init__(self, dictionary):
        self.__dict__.update(dictionary)
        for k, v in dictionary.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)


# *************** DEBUG ********************* #
def sql_debug(response):
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement.replace('?', '%s') % q.parameters).replace('\n', '\n       ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

    LoggerService.instance().debug('=' * 80)
    LoggerService.instance().debug(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    LoggerService.instance().debug('=' * 80)
    LoggerService.instance().debug(query_str.rstrip('\n'))
    LoggerService.instance().debug('=' * 80)
    return response
