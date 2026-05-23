from datetime import datetime


class User:
    def __init__(self, username, email, role) -> None:
        self.id = None
        self.username = username
        self.email = email
        self.role = role
        self.registration_date = datetime.now()

    def update_info(self, username=None, email=None, role=None):
        if username:
            self.username = username
        if email:
            self.email = email
        if role:
            self.role = role

    def to_dict(self):
        return self.__dict__.copy()
