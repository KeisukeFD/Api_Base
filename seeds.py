from flask_script import Command
from app import db
from models.admin.User import Role, User


# **** Add Seed command **** #
class Seed(Command):
    def run(self):
        # Roles
        role1 = Role(name="Admin")
        db.session.add(role1)

        # Users
        user1 = User("admin", "admin@test.tld", "1234")
        user1.roles.append(role1)
        db.session.add(user1)
        db.session.commit()
