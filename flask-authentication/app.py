import os, sys, base64, hashlib

from flask import Flask, request, session, jsonify, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from werkzeug.wrappers import Response
from models.user import User
from db.db import DB

from modules.crypt.rsaManager import RSAManager
from modules.crypt.aesManager import AESManager
from modules.crypt.authSecurity import AuthSecurity


app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

AES_KEY = b'd\xd6\xe1u\xc6P\xde\xee\xf0\x04zS\x05]\xcc.'

USERDB = DB('user')
POSTDB = DB('post')

# Flask-Login을 위한 사용자 로더 함수
@login_manager.user_loader
def user_loader(user_id: str) -> User:
    return User(*USERDB.select(user_id).values())

# Unauthorized Handler
@login_manager.unauthorized_handler
def unauthorized() -> Response:
    return redirect('/unauthorized')

# 인덱스 페이지 렌더링
@app.route('/', methods=['GET'])
def indexPage():
    return redirect('main' if current_user else 'login')

# 로그인 페이지 렌더링
@app.route('/login', methods=['GET'])
def loginPage():
    private_key, public_key = RSAManager.init()
    session['private_key'] = private_key
    
    return render_template('login.html', public_key=public_key.decode())

# 회원가입 페이지 렌더링
@app.route('/register', methods=['GET'])
def registerPage():
    private_key, public_key = RSAManager.init()
    session['private_key'] = private_key
    
    return render_template('register.html', public_key=public_key.decode())

# 메인 페이지 렌더링
@app.route('/main', methods=['GET'])
@login_required
def mainPage():
    return render_template('main.html')

# 401 페이지 렌더링
@app.route('/unauthorized', methods=['GET'])
def unauthorizedPage():
    return render_template('unauthorized.html')

# 로그인 API 엔드포인트
@app.route('/api/login', methods=['POST'])
def login():    
    private_key = session['private_key']
    user_id = RSAManager.decrypt(request.json['user_id'], private_key)
    user_pwd = RSAManager.decrypt(request.json['user_pwd'], private_key)
    
    user = user_loader(AuthSecurity.defaultEncrypt(user_id, AES_KEY))
    if user.get_id() not in USERDB:
        # user가 DB에 없는 경우
        json_res = { 'ok': False, 'error': 'Invalid ID or Password1.' }
        
    elif not user.can_login(AuthSecurity.passwordEncrypt(user_pwd)):
        # ID와 비밀번호가 매칭되지 않는 경우
        json_res = { 'ok': False, 'error': 'Invalid ID or Password2.' }
        
    else:
        json_res = { 'ok': True, 'msg': f'user <{user_id}> logined' }
        
        user = User(*USERDB.select(user.get_id()).values())
        user.authenticated = True
        USERDB.insert(user.get_id(), user.serialize())
        
        login_user(user, remember=True)
        
    return jsonify(json_res)

# 회원가입 API 엔드포인트
@app.route('/api/register', methods=['POST'])
def register():
    private_key = session['private_key']
    
    user_id = RSAManager.decrypt(request.json['user_id'], private_key)
    user_pwd = RSAManager.decrypt(request.json['user_pwd'], private_key)
    email = RSAManager.decrypt(request.json['email'], private_key)
    
    user = User(
        AuthSecurity.defaultEncrypt(user_id, AES_KEY),
        AuthSecurity.passwordEncrypt(user_pwd),
        AuthSecurity.defaultEncrypt(email, AES_KEY)
    )
    
    if USERDB.where('user_id', user.get_id()) != -1: # 이미 존재하는 UserID일 경우
        json_res = { 'ok': False, 'error': 'User ID Duplicated.' }
    else:
        json_res = { 'ok': True, 'msg': f'User <{user_id}> Added.' }
        USERDB.insert(user.get_id(), user.serialize())
    return jsonify(json_res)

# 로그아웃 API 엔드포인트
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    json_res = { 'ok': True, 'msg': f'user <{AuthSecurity.defaultDecrypt(user.user_id, AES_KEY)}> logout' }
    logout_user()
    return jsonify(json_res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
