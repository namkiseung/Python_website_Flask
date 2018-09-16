
from flask import Flask, request, session, g, render_template
import sqlite3, hashlib

app = Flask(__name__)
app.secret_key = 'a'
DATABASE = './db/user.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        f = open('schema.sql', 'r')
        db.execute(f.read())
        db.commit()
        db.close()

def save_user(ar_id, ar_pw, ar_name, ar_email, ar_phone):
    sql = 'INSERT INTO users (id, pw, name, email, phone) VALUES("{}", "{}", "{}", "{}", "{}")'.format(ar_id, ar_pw, ar_name, ar_email, ar_phone)
    db = get_db()
    db.execute(sql)
    db.commit()
    db.close()
    return ''

def get_user(idd, pw):
    pw = hash_224(pw)
    sql = 'SELECT * FROM users where id="{}" and pw="{}"'.format(idd, pw)
    db = get_db()
    rv = db.execute(sql)
    basic_res = rv.fetchall() 
    return basic_res

def all_get_user():
    sql = 'SELECT * FROM users'
    db = get_db()
    rv = db.execute(sql)
    allres = rv.fetchall()
    return allres

def hash_224(data):
    result = hashlib.sha224(data).hexdigest()
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        logon_id = request.form.get('user_id','')
        logon_pw = request.form.get('user_pw','')
        session['id'] = logon_id
        session['pw'] = logon_pw
        #session['user_email'] = ret[0][2]
        if session['id'] is not None:
            return render_template('login.html', data=session['id'], name=logon_id)
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    elif request.method == 'POST':
        in_new_id = request.form.get('new_id', '')
        in_new_pw = hash_224(request.form.get('new_pw', ''))
        in_new_name = request.form.get('new_name', '')
        in_new_email = request.form.get('new_email', '')
        in_new_phone = request.form.get('new_phone', '')
                
        save_user(ar_id=in_new_id, ar_pw=in_new_pw, ar_name=in_new_name, ar_email=in_new_email, ar_phone=in_new_phone)
        return '<a href="/">continue</a>'

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('id')
    session.pop('pw')
    return '<a href="/">continue</a>'

@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    a=all_get_user()
    print a[0][0], a[0][1], a[0][2]
    if request.method == 'POST':
        return request.form.get('name')+request.form.get('email')+ request.form.get('phone')
    if session['id'] is not None:
        r=get_user(session['id'], session['pw'])
        return render_template('mypage.html',update_id=r[0][0], update_pw=r[0][1], update_name=r[0][2], update_email=r[0][3], update_phone=r[0][4]) 
    return '<h1>Not Page</h1>'

@app.route('/main', methods=['GET', 'POST'])
def main():
    return 'hi'


if __name__ == '__main__':
    #init_db()
    app.run(debug=True, host='0.0.0.0', port=1111)
