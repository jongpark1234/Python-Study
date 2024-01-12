import os, sys
from flask import Flask, request, jsonify, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from werkzeug.wrappers import Response
from model.user import User
from config.config import USERS

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

# Flask-Login을 위한 사용자 로더 함수
@login_manager.user_loader
def user_loader(user_id: str) -> User:
    return USERS[user_id]

# Unauthorized Handler
@login_manager.unauthorized_handler
def unauthorized() -> Response:
    return redirect('/unauthorized')

# 인덱스 페이지 렌더링
@app.route('/', methods=['GET'])
def indexPage():
    return redirect('main')

# 로그인 페이지 렌더링
@app.route('/login', methods=['GET'])
def loginPage():
    return render_template('login.html')

# 메인 페이지 렌더링
@app.route('/main', methods=['GET'])
@login_required
def mainPage():
    return render_template('main.html')

# 401 페이지 렌더링
@app.route('/unauthorized', methods=['GET'])
def unauthorizedPage():
    return render_template('unauthorized.html')

# 사용자 추가 API 엔드포인트
@app.route('/api/add_user', methods=['POST'])
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

# 로그인 API 엔드포인트
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
    json_res = { 'ok': True, 'msg': f'user <{user.user_id}> logout' }
    logout_user()
    return jsonify(json_res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
