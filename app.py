import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_json_schema import JsonSchema, JsonValidationError

app = Flask(__name__)
schema = JsonSchema(app)


# **** error handler for json schema **** #
@app.errorhandler(JsonValidationError)
def validation_error(e):
    from utils.shortcuts import error
    return error([e.message]+[error.message for error in e.errors])


# **** Getting Environment mode **** #
app_env = os.environ.get('FLASK_ENV') or 'development'
if app_env == 'production':
    app.config.from_object('configs.production.ProductionConfig')
if app_env == 'development':
    app.config.from_object('configs.development.DevelopmentConfig')

# **** Loading SQL Config **** #
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app.config['TRACK_DB_MODIFICATIONS']

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
config = app.config

from services.loggers import LoggerService
LoggerService.initialize(config['LOGGERS'])

# **** Loading routes **** #
from admin import default as default_admin
app.register_blueprint(default_admin.bp, url_prefix=config['ADMIN_PREFIX'])
from admin import users as admin_users
app.register_blueprint(admin_users.bp, url_prefix='%s/users' % config['ADMIN_PREFIX'])

from routes import default
app.register_blueprint(default.bp, url_prefix='/')


# ********* SQL Debug ********* #
if app.debug:
    from utils.functions import sql_debug
    app.after_request(sql_debug)

# **** Running App **** #
if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
