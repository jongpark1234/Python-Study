class User:
    def __init__(self, user_id: str, user_pwd: str=None, email: str=None, authenticated: bool=False):
        self.user_id = user_id
        self.user_pwd = user_pwd
        self.email = email
        self.authenticated = authenticated

    def __repr__(self):
        return str({
            'user_id': self.user_id,
            'user_pwd': self.user_pwd,
            'email': self.email,
            'authenticated': self.authenticated,
        })

    def can_login(self, user_pwd):
        return self.user_pwd == user_pwd

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False