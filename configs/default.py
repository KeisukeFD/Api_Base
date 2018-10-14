class Config:
    APP_NAME = 'API_BASE'
    HOST = '127.0.0.1'
    PORT = 5000

    BASE_URL = 'http://127.0.0.1:5000/'

    ADMIN_PREFIX = '/admin'

    TAXES = {
        'PST': 0.09975,
        'GST': 0.05
    }

    # # Python Logging
    LOGGERS = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    }
