# -*- coding:utf-8 -*-
from flask import Flask, g, request, render_template, url_for
import sqlite3

DATABASE='./db/test.db'
app = Flask(__name__)

def get_db():
   db = getattr(g, '_database', None)
   if db is None:
     db = g._database = sqlite3.connect(DATABASE)
     return db

def init_db():
   with app.app_context():
      with open('schema.sql', 'r') as f:
         db = get_db()
         db.cursor().executescript(f.read())
         db.commit()
   return ''

def member_insert(argsid='', argsname='', argspasswd='', argsemail=''):
    db = get_db()
    sql = 'INSERT INTO users (id, name, passwd, email) VALUES ("{}", "{}", "{}", "{}")'.format(argsid, argsname, argspasswd, argsemail)
    res = db.execute(sql)
    db.commit()
    db.close()
    return ''

def select_info():
    db = get_db()
    sql = 'SELECT * FROM users'
    res=db.execute(sql)
    return res[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
       return render_template('login.html')
    else:
       input_userid=request.form.get('user_id')
       input_userpw=request.form.get('user_pw')
       return render_template('home.html', current_userinfo=input_userid)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        get_id = request.form.get('user_id')
        get_pw =  request.form.get('user_pw')
        get_name = request.form.get('user_name')
        get_email = request.form.get('user_email')
        member_insert(argsid=get_id, argspasswd=get_pw, argsname=get_name, argsemail=get_email)
        return render_template('login.html')

@app.route('/home')
def home():
   getusers = select_info()
   return render_template('home.html', dbusers=getusers)


if __name__ == "__main__":
   #init_db()
   app.run(debug=True, host='0.0.0.0', port=1111)
