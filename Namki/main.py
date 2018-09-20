#-*- coding=utf-8 -*-
from flask import Flask, request, session, g, render_template, redirect, url_for
from flask_basicauth import BasicAuth
from werkzeug import secure_filename
import sqlite3, hashlib, os, datetime

app = Flask(__name__)
now = datetime.datetime.now()
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '0000'
#'adc91e03060b42e7836bdfba7ce19b3bc1297d234fec44585472529d'
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = False
app.secret_key = 'a'
DATABASE = './db/user.db'
DATABASEnotice = './db/noticeboard.db'


@app.route('/admin')
@basic_auth.required
def admin_access():
    r = all_get_user()
    return render_template('admin.html', user_info=r)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def get_dbnotice():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASEnotice)
    return db

def exist_db():
    if os.path.exists("./db/user.db") is not True:
        init_db()
    if os.path.exists("./db/noticeboard.db") is not True:
        init_db_notice()    
    return ''

def init_db():
    with app.app_context():
        db = get_db()
        f = open('schema.sql', 'r')
        db.execute(f.read())
        db.commit()
        db.close()

def init_db_notice():
    with app.app_context():
        db = get_dbnotice()
        f = open('noticeboard.sql', 'r')
        db.execute(f.read())
        db.commit()
        db.close()

def save_noticedb(idid="",title="",content="",day="",files=""):
     sql = 'INSERT INTO notice_board (id, title, content, day, files) VALUES ("{}","{}","{}","{}","{}")'.format(idid,title,content,day,files)
     db = get_dbnotice()
     db.execute(sql)
     db.commit()
     db.close()
     return ''

def get_noticedb_list():    
    sql = 'SELECT * FROM notice_board'#.format(idx_number)
    db = get_dbnotice()
    rv = db.execute(sql)
    res = rv.fetchall() 
    return res

def get_noticedb_read(idx_number):    
    sql = 'SELECT * FROM notice_board where idx="{}"'.format(idx_number)
    db = get_dbnotice()
    rv = db.execute(sql)
    res = rv.fetchall() 
    return res

# def update_user(n_name=None, n_email=None, n_phone=None):
#     if n_name is not None and n_email is not None and n_phone is not None:
#        db = get_db()
#        #r = get_user()
#        print n_name
#        print n_email
#        print n_phone
#        sql = 'UPDATE users set name="{}", email="{}", phone="{}" where id="{}" '.format(n_name, n_email, n_phone, session['id']) 
#        rv = db.execute(sql)
#        db.commit()
#        db.close()
#     return ''

# def delete_user(bye_user):
#     db = get_db()
#     sql = 'DELETE FROM users where id="{}"'.format(bye_user)
#     logout()
#     rv = db.execute(sql)
#     db.commit()
#     db.close()
#     return ''

def save_user(ar_id, ar_pw, ar_name, ar_email, ar_phone):
    sql = 'INSERT INTO users (id, pw, name, email, phone) VALUES("{}", "{}", "{}", "{}", "{}")'.format(ar_id, ar_pw, ar_name, ar_email, ar_phone)
    db = get_db()
    db.execute(sql)
    db.commit()
    db.close()
    return ''

def get_user(idd, pwago):
    pw = hash_224(pwago)
    sql = 'SELECT * FROM users where id="{}" and pw="{}"'.format(idd, pw)
    db = get_db()
    rv = db.execute(sql)
    basic_res = rv.fetchall() 
    if basic_res is None:
        return False    
    return basic_res

def get_user_single(idd, pwago):
    pw = hash_224(pwago)
    sql = 'SELECT * FROM users where id="{}" and pw="{}"'.format(idd, pw)
    db = get_db()
    rv = db.execute(sql)
    res = rv.fetchone() 
    if res is None:
        return False    
    return True

def all_get_user():
    sql = 'SELECT * FROM users'
    db = get_db()
    rv = db.execute(sql)
    allres = rv.fetchall()
    return allres

def hash_224(data):
    result = hashlib.sha224(data).hexdigest()
    return result

def update_user(n_name=None, n_email=None, n_phone=None):
    if n_name is not None and n_email is not None and n_phone is not None:
       db = get_db()
       #r = get_user()
       print n_name
       print n_email
       print n_phone
       sql = 'UPDATE users set name="{}", email="{}", phone="{}" where id="{}" '.format(n_name, n_email, n_phone, session.get('id')) 
       rv = db.execute(sql)
       db.commit()
       db.close()
    return ''

def delete_user(bye_user):
    db = get_db()
    sql = 'DELETE FROM users where id="{}"'.format(bye_user)
    logout()
    rv = db.execute(sql)
    db.commit()
    db.close()
    return ''

@app.route('/', methods=['GET', 'POST'])
def menetory():
    if session.get('id') is not None:
        "<script>alert('welcome!';)</script>"
        return redirect(url_for('me_list'))
    return redirect(url_for('login')) #Hello {}'.format(session['id'])


@app.route('/login_chk', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if session.get('id') is not None:
            return redirect(url_for('login'))
        return render_template('login.html')
    elif request.method == 'POST':
        logon_id = request.form.get('user_id','')
        logon_pw = request.form.get('user_pw','')        
        chk_r=get_user_single(logon_id, logon_pw)                
        if chk_r is True:
            r=get_user(logon_id, logon_pw)
            session['id'] = r[0][0]
            session['pw'] = r[0][1]         
            session['name'] = r[0][2]            
            session['email'] = r[0][3]
            session['phone'] = r[0][4]                                     
    return redirect(url_for('menetory'))

@app.route('/login')
def login():    
    if session.get('id') is not None:
        return redirect(url_for("menetory"))
    return render_template('login.html')    

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
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    if session.get('id') is None:
        return redirect(url_for('login'))
    else:
        for x in ['id', 'pw', 'name', 'email', 'phone']:
            session.pop(x)
            print x
        return redirect(url_for('login'))

@app.route('/delete_user')
def delete_user_action():
    delete_user(bye_user=session.get('id'))
    return '<h1>User Info Delete success!!</h1><br><a href="/">continue</a>'

@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if request.method == 'POST':
        update_user(n_name=request.form.get('name'), n_email=request.form.get('email'), n_phone=str(request.form.get('phone')))
        return '<h1>User Info Update success!!</h1><br><a href="/">continue</a>'
    if session.get('id') is not None:
        r=get_user(session.get('id'), session.get('pw'))
        return render_template('mypage.html',update_id=r[0][0], update_pw=r[0][1], update_name=r[0][2], update_email=r[0][3], update_phone=r[0][4]) 
    return '<h1>Not Page</h1>'

@app.route('/list', methods=['GET', 'POST'])
def me_list():
    if session.get('id') is None:
        return redirect(url_for('login'))
    r=get_noticedb_list()        
    return render_template('list.html', data = r)
 
@app.route('/read', methods=['GET', 'POST'])
def me_read():
    if request.args.get('num') is not None:
        r=get_noticedb_read(idx_number=request.args.get('num'))
        print '#####################'
        print r[0][2]
        print '#####################'
        return render_template('read.html', search = r)
    return render_template('read.html')

@app.route('/write', methods=['GET', 'POST'])
def me_write():
    if request.method == "GET":
        return render_template('write.html', userid=session.get('id'))
    elif request.method == "POST":        
        writer = session.get('id')
        save_title=request.form.get('notitle')
        save_content=request.form.get('nocontent')
        save_day=now.strftime('%Y-%m-%d %H:%M:%S')
        #f = request.files['_file']
        #f.save('./uploads' + secure_filename(f.filename))
        save_files=request.form.get('_file')
        save_noticedb(idid=writer, title=save_title,content=save_content, day=save_day, files=save_files)
        return redirect(url_for('me_list'))
    return ''

if __name__ == '__main__':
    exist_db()    
    # init_db_notice()
    app.run(debug=True, host='0.0.0.0', port=1111)
