import os
from flask import Flask, request, jsonify, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

# 사용자 정보를 저장하는 간단한 사용자 클래스
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

# 더미 사용자 데이터베이스
USERS = {
    'jongpark1234': User('jongpark1234', '1234'),
}

# Flask-Login을 위한 사용자 로더 함수
@login_manager.user_loader
def user_loader(user_id):
    return USERS[user_id]

@app.route("/", methods=['GET'])
def indexPage():
    return redirect('main')

# 로그인 페이지 렌더링
@app.route("/login", methods=['GET'])
def loginPage():
    return render_template('login.html')

@app.route("/main", methods=['GET'])
def mainPage():
    return render_template('main.html')

# 사용자 추가 API 엔드포인트
@app.route("/api/add_user", methods=['POST'])
def addUser():
    user_id = request.json['user_id']
    user_pwd = request.json['user_pwd']
    if user_id in USERS:
        json_res = {'ok': False, 'error': f'user <{user_id}> already exists'}
    else:
        user = User(user_id, user_pwd)
        USERS[user_id] = user
        json_res = {'ok': True, 'msg': f'user <{user_id}> added'}
    return jsonify(json_res)

# Login API Endpoint
@app.route('/api/login', methods=['POST'])
def login():
    user_id = request.json['user_id']
    user_pwd = request.json['user_pwd']
    if user_id not in USERS:
        json_res = {'ok': False, 'error': 'Invalid user_id or password'}
    elif not USERS[user_id].can_login(user_pwd):
        json_res = {'ok': False, 'error': 'Invalid user_id or password'}
    else:
        json_res = {'ok': True, 'msg': f'user <{user_id}> logined'}
        USERS[user_id].authenticated = True
        login_user(USERS[user_id], remember=True)
    return jsonify(json_res)

# 로그아웃 API 엔드포인트
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    json_res = {'ok': True, 'msg': f'user <{user.user_id}> logout'}
    logout_user()
    return jsonify(json_res)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)