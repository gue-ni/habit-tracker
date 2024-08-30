from flask_login import UserMixin
from . import db

class User(UserMixin):
    def __init__(self, id, name):
        self.id = str(id)
        self.name = name
        self.authenticated = False

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

