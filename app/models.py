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

    def is_admin(self):
        return int(self.id) == 1


class AppException(Exception):
    def __init__(self, message, status_code):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        # Store custom attributes
        self.status_code = status_code

    def __str__(self):
        # Return a custom error message with the error code
        return f"{self.args[0]} (Error Code: {self.status_code})"
