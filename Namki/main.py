#-*- coding=utf-8 -*-
from flask import Flask, request, session, g, render_template, redirect, url_for, send_from_directory
from flask_basicauth import BasicAuth
from werkzeug import secure_filename
import sqlite3, hashlib, os, datetime
from bs4 import BeautifulSoup 
import lxml, requests
#print os.popen('apt install ntpdate').read()
#print os.popen('chkconfig ntpd on').read()
#print os.popen('service ntpd restart').read()
#print os.popen('ntpq -dp').read()
#print os.popen('crontab -e').read() #-> 00 01 * * * ntpdate time.bora.net

app = Flask(__name__)
# now = datetime.datetime.now()
# print type(now)
# nowday=now.strftime('%Y-%m-%d %H:%M:%S')
def day():
    commend_date = os.popen('date').read()
    now=commend_date.split()
    nowday=now[5]+"-"+now[1]+"-"+now[2]+" "+now[3] 
    return nowday

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '0000'
#'adc91e03060b42e7836bdfba7ce19b3bc1297d234fec44585472529d'
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = False
app.secret_key = day()
DATABASE = './db/user.db'
DATABASEnotice = './db/noticeboard.db'
DATABASEnotice_re = './db/noticeboard_re.db'
DATABASEnotice_re2 = './db/noticeboard_re2.db'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'png', 'gif'])


@app.route('/manage/')
@basic_auth.required
def admin_access():
    r = all_get_user()
    return render_template('admin.html', user_info=r)

@app.route('/manage/notice')
@basic_auth.required
def admin_access2():
    return render_template('manage.html')

def day_date():
    commend_date = os.popen('date').read()
    now=commend_date.split()
    nowday=now[5]+"-"+now[1]+"-"+now[2]+" "+now[3] 
    return nowday

#파일업로드
def allowed_file(filename):
    return './uploads' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

def get_dbnotice_re():
    db = getattr(g, '_database_re', None)
    print "!!!!!!!!!!!!!!"
    if db is None:
        print "!!!!!!!!!!!!!!~~~"
        db = g._database_re = sqlite3.connect(DATABASEnotice_re)
    return db

def get_dbnotice_re2():
    db = getattr(g, '_database_re2', None)
    if db is None:
        db = g._database_re2 = sqlite3.connect(DATABASEnotice_re2)
    return db

def exist_db():
    if os.path.exists("./db/user.db") is not True:
        init_db()
    if os.path.exists("./db/noticeboard.db") is not True:
        init_db_notice()    
    if os.path.exists("./db/noticeboard_re.db") is not True:
        init_db_notice_re() 
    if os.path.exists("./db/noticeboard_re2.db") is not True:
        init_db_notice_re2() 
    return ''

def script_alert(msg):
    messages = "<script type='text/javascript'>alert('{}');</script>".format(msg)
    return messages

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

def init_db_notice_re():
    with app.app_context():
        db = get_dbnotice_re()
        f = open('noticeboard_re.sql', 'r')
        db.execute(f.read())
        db.commit()
        db.close()
###########################################################################################
def init_db_notice_re2():
    with app.app_context():
        db = get_dbnotice_re2()
        f = open('noticeboard_re2.sql', 'r')
        db.execute(f.read())
        db.commit()
        db.close()
   
###########################################################################################
def search_board(text="", select=""):
    if select == "title":
        sql = 'SELECT * FROM notice_board WHERE title like "{}%" ORDER BY day desc'.format(text)
    elif select == "writer": 
        sql = 'SELECT * FROM notice_board WHERE id="{}" ORDER BY day desc'.format(text)
    db = get_dbnotice()
    rv = db.execute(sql)
    res = rv.fetchall()
    return res

def select_countview(idx=""):
    sql = 'SELECT countview FROM notice_board WHERE idx="{}"'.format(idx)
    db = get_dbnotice()
    rv = db.execute(sql)
    res = rv.fetchall()
    return res[0][0]

def save_countview(count="", idx=""):
    sql = 'UPDATE notice_board SET countview="{}" WHERE idx="{}"'.format(count, idx)
    db = get_dbnotice()
    db.execute(sql)
    db.commit()
    db.close()
    return ''

def save_noticedb(idid="",title="",content="",day="",files=""):
    sql = 'INSERT INTO notice_board (id, title, content, day, files) VALUES ("{}","{}","{}","{}","{}")'.format(idid,title,content,day,files)
    db = get_dbnotice()
    db.execute(sql)
    db.commit()
    db.close()
    return ''

def get_noticedb_list():    
    sql = 'SELECT * FROM notice_board ORDER BY day desc'#.format(idx_number)
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

def update_noticedb(idx="", idid="",title="",content="",day="",files=""):    
    db = get_dbnotice()
    sql = 'UPDATE notice_board set id="{}", title="{}", content="{}", day="{}", files="{}" WHERE idx="{}"'.format(idid,title,content,day,files, idx)
    rv = db.execute(sql)
    db.commit()
    db.close()
    return ''

def delete_noticedb(idx=""):
    db = get_dbnotice()    
    sql = 'DELETE FROM notice_board WHERE idx="{}"'.format(idx)
    db.execute(sql)    
    db2=get_dbnotice_re()
    sql2 = 'DELETE FROM notice_board_re WHERE originidx="{}"'.format(idx)
    db2.execute(sql2)    
    db.commit()
    db2.commit()
    db.close()
    db2.close()
    return ''

# def board_delete(idx=""):
#     db = get_dbnotice()
#     sql = 'DELETE FROM notice_board_re WHERE idx="{}"'.format(idx)
#     rv = db.execute(sql)
#     db.commit()
#     db.close()
#     return ''
####################################################################
def save_noticedb_re(readidx="", userid="", content="", day=""):
     sql = 'INSERT INTO notice_board_re (originidx, id, content, day) VALUES ("{}","{}","{}","{}")'.format(readidx, userid, content, day)
     db = get_dbnotice_re()
     db.execute(sql)
     db.commit()
     db.close()
     return ''

def get_noticedb_list_re(num):    
    db = get_dbnotice_re()
    sql = 'SELECT * FROM notice_board_re WHERE originidx="{}" ORDER BY day desc'.format(num)    
    rv = db.execute(sql)
    res = rv.fetchall()  
    # chk = rv.fetchone()         
    return res

# def get_noticedb_read(idx_number):    
#     sql = 'SELECT * FROM notice_board_re where idx="{}"'.format(idx_number)
#     db = get_dbnotice_re()
#     rv = db.execute(sql)
#     res = rv.fetchall() 
#     return res

# def update_noticedb(idx="", idid="",title="",content="",day="",files=""):    
#     db = get_dbnotice_re()
#     sql = 'UPDATE notice_board_re set id="{}", title="{}", content="{}", day="{}", files="{}" WHERE idx="{}"'.format(idid,title,content,day,files, idx)
#     rv = db.execute(sql)
#     db.commit()
#     db.close()
#     return ''

def delete_noticedb_re(idx_1="", idx_2=""):
    db = get_dbnotice_re()
    sql = 'DELETE FROM notice_board_re where idx="{}" and originidx="{}"'.format(idx_1, idx_2)
    rv = db.execute(sql)
    db.commit()
    db.close()
    return ''
####################################################################
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

def menubar():
    if session.get('id') is None:
        return False
    return True
################################################################################
@app.route('/', methods=['GET', 'POST'])
def menetory():
    if session.get('id') is not None:
        "<script>alert('welcome!';)</script>"
        return redirect(url_for('me_list'))
    return redirect(url_for('login')) #Hello {}'.format(session['id'])


@app.route('/login_chk', methods=['POST'])
def index():
    if request.method == 'POST':
        logon_id = request.form.get('user_id','')
        logon_pw = request.form.get('user_pw','')        
        chk_r=get_user_single(logon_id, logon_pw)                
        if chk_r is True:
            r=get_user(logon_id, logon_pw)
            session['id'] = r[0][0]
            session['pw'] = hash_224(r[0][1])
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
    script_alert("bye-bye")
    redirect(url_for('login'))

@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if request.method == 'POST':
        update_user(n_name=request.form.get('name'), n_email=request.form.get('email'), n_phone=str(request.form.get('phone')))
        return redirect(url_for('me_read'))
    elif request.method == 'GET':
        return render_template('mypage.html',update_id=session.get('id'), update_name=session.get('name'), update_email=session.get('email'), update_phone=session.get('phone'), logon = menubar()) 
    return '<h1>Not Page</h1>'

@app.route('/list', methods=['GET', 'POST'])
def me_list():        
    r=get_noticedb_list()
    text=request.args.get('searchtext')
    category=str(request.args.get('category'))
    if request.method == "GET" and request.args.get('category') is not None:
        r = search_board(text=text, select=category)
    idx_num=len(r)        
    if session.get('id') is None:
        return render_template('list.html', data = r, length = idx_num)           
    return render_template('list.html', data = r, logon = menubar(), length = idx_num)
 
@app.route('/read', methods=['GET', 'POST'])
def me_read(num=None):    
    if request.args.get('num') is not None and request.method == 'GET':
        idx=request.args.get('num')
        r=get_noticedb_read(idx_number=idx)
        rt = get_noticedb_list_re(idx)          
        count=select_countview(idx)
        count = count+1
        save_countview(count=count, idx=idx)
        return render_template('read.html', search = r, logon = menubar(), user = session.get('id'), writerid=r[0][1], data_re=rt, currentpage=idx)    
    if request.method == 'POST':
        ori_num=request.form.get('currentPage') #게시글 idx번호
        repple=request.form.get('commentContent')
        print ori_num
        print repple
        save_noticedb_re(readidx=ori_num, userid=session.get('id'), content=repple, day=day_date())
    return redirect(url_for('me_read', num=ori_num)) #"<script>history.go(-1);</script>" #redirect(url_for('me_read'))

# @app.route('/rep_update', methods=['GET', 'POST'])
# def reupdate():
#     return redirect(url_for('me_list'))

@app.route('/rep_delete', methods=['GET', 'POST'])
def reupdate(): #, currentpage=None
    delnum=request.args.get('delnum')
    currentpage=request.args.get('currentpage')
    delete_noticedb_re(idx_1=delnum, idx_2=currentpage)
    script_alert("success repple delete")
    return redirect(url_for('me_read', num=currentpage))

@app.route('/update', methods=['GET', 'POST'])
def me_update():    
    if request.method == "GET" and session.get('id') is not None:               
        r=get_noticedb_read(idx_number=request.args.get('num'))    
        return render_template('update.html', writerid=r[0][1], usertitle=r[0][2], usercontent=r[0][3], logon = menubar(), user=session.get('id'), textnum=r[0][0])
    elif request.method == "POST":          
        r=get_noticedb_read(idx_number=request.form.get('textnum'))   
        save_title=request.form.get('notitle')
        save_content=request.form.get('nocontent')
        save_files=request.form.get('_file')                        
        update_noticedb(idid=r[0][1], title=save_title,content=save_content, day=day_date(), files=save_files, idx=r[0][0])
        return redirect(url_for('me_list'))
    return ''

@app.route('/delete', methods=['GET'])
def me_delete():    
    if session.get('id') is not None:        
        if request.args.get('num') is not None:  #    request.method == "GET":            
            delete_noticedb(idx=request.args.get('num'))            
            script_alert('success. have a good time')
    return redirect(url_for('me_list'))

@app.route('/write', methods=['GET', 'POST'])
def me_write():
    if request.method == "GET":
        return render_template('write.html', userid=session.get('id'))
    elif request.method == "POST":        
        writerid = session.get('id')
        save_title=request.form.get('notitle')
        save_content=request.form.get('nocontent')
        #file = request.files['_file']
        #if file and allowed_file(file.filename):
        #    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        #    filename = secure_filename(file.filename)
        #    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #send_from_diretory(app.config['UPLOAD_FOLDER'], filename)
        save_files=request.form.get('_file')
        save_noticedb(idid=writerid, title=save_title,content=save_content, day=day_date(), files=save_files)
        return redirect(url_for('me_list'))
    return ''



if __name__ == '__main__':
    exist_db()        
    app.run(debug=True, host='0.0.0.0', port=1111)
