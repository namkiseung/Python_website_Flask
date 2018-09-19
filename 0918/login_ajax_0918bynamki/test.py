#-*- coding:utf-8 -*-
from flask import Flask, session, redirect, request, g, render_template, url_for
import sqlite3

app = Flask(__name__)
DATABASE='./test.db'
app.secret_key='a'

def get_db():
   db = getattr(g, '_database', None)
   if db is None:
       db = g._database = sqlite3.connect(DATABASE)
   return db

@app.route('/')
def menetory():
    if session.get('id') is None:
        return redirect(url_for('go_login'))
    return 'Hello {}'.format(session['id'])

@app.route('/login', methods=['GET', 'POST'])
def go_login():
    if session.get('id') is not None:
        return redirect(url_for('menetory'))
    if request.method == 'GET':
        return render_template('login.html')
    return render_template('login.html')

@app.route('/login_chk', methods=['GET', 'POST'])
def usercheck():
    userid = request.form.get('user_id', '')
    userpw = request.form.get('user_pw', '')
    a=get_user(idid=userid, pw=userpw)
    print userid
    print userpw
    print a
    if a is True:
        session['id']=userid
        return redirect(url_for('menetory'))
    #try:
    #    session['id']=a[0][0]
    #except IndexError:
    #    session['id']=None       
    #print '##################'
    #print a[0][0]
    return redirect(url_for('go_login'))

def get_user(idid, pw):
    sql_query = 'SELECT * FROM users where id="{}" and pw="{}"'.format(idid, pw)
    db = get_db()
    rv = db.execute(sql_query)
    #try:
    #   res = rv.fetchall()
    #except IndexError:
    #   res = []
    res=rv.fetchone()
    print "####"
    print res
    print "######"
    if res is None:
        return False
    return True

@app.route('/logout')
def logout():
    if session.get('id') is not None:
       session.pop('id')
       return redirect(url_for('go_login'))
    else:
       return redirect(url_for('go_login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1111)
