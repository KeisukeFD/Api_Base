from .default import Config


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite:///dev.db'
    TRACK_DB_MODIFICATIONS = True
    SECRET_KEY = 'development key'
