from flask_login import UserMixin
class User():
    def __init__(self, 
                 user_id: str, 
                 user_pwd: str = None, 
                 email: str = None, 
                 active: bool = True,
                 anonymous: bool = False
                ):
        self.user_id = user_id
        self.user_pwd = user_pwd
        self.email = email
        self.active = active
        self.anonymous = anonymous

    def __repr__(self) -> dict:
        return str({
            'user_id': self.user_id,
            'user_pwd': self.user_pwd,
            'email': self.email,
            'active': self.active,
            'anonymous': self.anonymous,
        })
    
    def serialize(self) -> dict:
        return {
            'user_id': self.user_id,
            'user_pwd': self.user_pwd,
            'email': self.email,
            'active': self.active,
            'anonymous': self.anonymous,
        }
    
    def can_login(self, user_pwd):
        return self.user_pwd == user_pwd

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False