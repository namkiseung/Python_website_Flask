from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from member_db_app import *
from flask_sslify import SSLify
from OpenSSL import SSL
#context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
#context.use_privatekey_file('server.key')
#context.use_certificate_file('server.crt')
db = SQLAlchemy()
app = Flask(__name__)
sslify = SSLify(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/member.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "abcde"
db = SQLAlchemy(app)

@app.route('/')
def index():
   if session.get('id') is None:
      return redirect(url_for('m_login'))
   else:
      return 'success login'+"<a href='http://192.168.0.209:1111/logout'><h1>  logout</h1></a>"

@app.route('/login', methods=['GET'])
def m_login():
   if session.get('id') is not None:
      return redirect(url_for('index'))
   return render_template('login.html')   

@app.route('/login_chk', methods=['POST'])  
def m_loginchk():   
   _user_id = request.form.get('user_id')
   _user_pass = request.form.get('user_pw')
   pass_check = verify_login(_username=_user_id, _password=_user_pass)
   print "@@@@@@@@@@@@@"
   print pass_check
   if pass_check is True:
      session['id'] = _user_id
      session['pw'] = _user_pass
      return redirect(url_for('index'))
   else:
      return redirect(url_for('m_login'))

@app.route('/logout')
def m_logout():
   session.pop('id')
   session.pop('pw')
   return redirect(url_for('m_login'))

if __name__=="__main__":
  #user_add('namki', 'rltmd1004@naver.com', '010-9406-5290', '1q2w3e4r', 'file:///a.jpg', 0)
  #db.init_app(app)
  app.run(debug=True, host="0.0.0.0", port=1111, threaded=True)#ssl_context=context

