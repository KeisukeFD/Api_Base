from .default import Config


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = 'database-uri-for-prod'
    TRACK_DB_MODIFICATIONS = False
    SECRET_KEY = 'production key'

    LOGGERS = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s: %(message)s',
            }
        },
        'handlers': {
            'to_file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'default',
                'filename': 'logs/%s.log' % Config.APP_NAME,
                'interval': 1,
                'when': 'M',
                'backupCount': 3
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['to_file']
        }
    }
