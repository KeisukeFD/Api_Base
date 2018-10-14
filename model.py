from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from seeds import Seed

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('seed', Seed())

# **** Import models from folder **** #
from models.admin.User import *
# Include others models you apps needs

# **** Manage migration from cmd **** #
if __name__ == '__main__':
    manager.run()
