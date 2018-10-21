#-*- coding:utf-8 -*-
from flask import Flask, request, session, g, render_template, redirect, url_for, send_from_directory, jsonify
from flask_basicauth import BasicAuth
from werkzeug import secure_filename
import sqlite3, hashlib, os, datetime, json
from bs4 import BeautifulSoup 
import lxml, requests, datetime#, socketio, eventlet
    #Using the ntp  protocol
    #print os.popen('apt install ntpdate').read()
    #print os.popen('chkconfig ntpd on').read()
    #print os.popen('service ntpd restart').read()
    #print os.popen('ntpq -dp').read()
    #print os.popen('crontab -e').read() #-> 00 01 * * * ntpdate time.bora.net
#sio = socketio.Server() #Server socket declaration
messages = [] #Leave messages as leading variables for notifications

app = Flask(__name__)# static_folder='uploads'
    #Using the datetime module
    

#It is used as a Linux command.
def day_date():
    #commend_date = os.popen('date').read() 
    #now=commend_date.split() #String separation
    #nowday=now[5]+"-"+now[1]+"-"+now[2]+" "+now[3] # example output) 2018-Seq-27 01:20:19    
    now = datetime.datetime.now()
    print type(now)
    nowday=now.strftime('%Y-%m-%d %H:%M:%S')
    return nowday

    # @sio.on('connect')
    # def connect(sid, env):
    #     print('connected %s' % sid)

    # @sio.on('send message')
    # def get_message(sid, data):
    #     sio.emit('new message', {
    #         "nickname": data["nickname"],
    #         "body": data["body"]
    #     }, skip_sid=sid)

    # @sio.on('disconnect')
    # def disconnect(sid):
    #     print('disconnected %s' % sid)
## static variable
UPLOAD_FOLDER = './uploads'  #Variable with path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['BASIC_AUTH_USERNAME'] = 'admin' #administrator ID of the object
app.config['BASIC_AUTH_PASSWORD'] = '0000' #administrator PW of the object
#'adc91e03060b42e7836bdfba7ce19b3bc1297d234fec44585472529d' #'0000' of sha224 value
basic_auth = BasicAuth(app) #Object for authentication
app.config['BASIC_AUTH_FORCE'] = False # True is to protect the site
app.secret_key = day_date() #Put date value random in variable called Key
DATABASE = './db/user.db' #users db file variable with path
DATABASEnotice = './db/noticeboard.db' #notice board db file variable with path
DATABASEnotice_re = './db/noticeboard_re.db'  #repple db file variable with path
DATABASEnotice_re2 = './db/noticeboard_re2.db' #Greate repple db file variable with path
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'png', 'gif']) #File extension list

######################################Admin page access processing routing#######################################
@app.route('/manage/')  #administrator default routing
@basic_auth.required  #When approaching demand.
def admin_access(): #administrator default func
    r = all_get_user() #This func that gets all of the user's info.
    return render_template('admin.html', user_info=r) #It brings out the main page

@app.route('/manage/notice') #administrator management board routing
@basic_auth.required
def manage_notice(): #administrator management board func
    r = get_noticedb_list() #board info get it(order)
    for x in range(len(r)):  
        print r[x]
    return render_template('manage.html', notice_info=r) 

@app.route('/manage/conversation', methods=['GET', 'POST']) #this is where to manage the menu called conversation
def manage_conversation(): #manage conversation menu func
    if request.method == "GET":  
        return render_template('manage_conversation.html')
    else: # To handle other http method.
        script_alert("Login is required.")       
        return redirect(url_for('/'))

@app.route('/manage/basic_crawl', methods=['GET']) #Route info to a scraping page
def issue_github(): #Func to get issus github of feather
   req = requests.get('https://github.com/trending/python?since=daily')
   html = req.text
   soup = BeautifulSoup(html, 'html.parser') 
   list_text=[]
   list_text2=[]
   result=[]
   for tag in soup.select('span[class="d-inline-block float-sm-right"]'):
       list_text.append(tag.text) 
   for tag2 in soup.select('span[class="text-normal"]'):
       list_text2.append(tag2.text) 
   print list_text2
   for x in range(len(list_text)):
       result.append(("",""))
   print result
   for x in range(len(list_text)):
       result[x]=((list_text[x],list_text2[x]))
       print result[x] 
   return render_template('crawl.html', data=result)
################################################################################################################################
def allowed_file(filename):  #string from the right at the specified separator and return a list of input files in func
    return './uploads' in filename and \
           filename.rsplit('.', 1)[1].lowor() in ALLOWED_EXTENSIONS   #The value returned is true or false

def script_alert(msg):
    messages = '<script>alert("{}");</script>'.format(msg)
    return messages

def hash_224(data):
    result = hashlib.sha224(data).hexdigest()
    return result

def menubar():
    if session.get('id') is None:
        return False
    return True
################################################################################################################################
## Where to prepare the objects in the DB(Database)
def get_db():  #Usage a USERS
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)   #'./db/user.db'
    return db

def get_dbnotice(): #Usage a notice board
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASEnotice)  #'./db/noticeboard.db'
    return db

def get_dbnotice_re(): #Usage a notice board at repple 
    db = getattr(g, '_database_re', None)
    if db is None:        
        db = g._database_re = sqlite3.connect(DATABASEnotice_re) #'./db/noticeboard_re.db'
    return db

def get_dbnotice_re2():  #Usage a notice board at great repple
    db = getattr(g, '_database_re2', None)
    if db is None:
        db = g._database_re2 = sqlite3.connect(DATABASEnotice_re2) #'./db/noticeboard_re2.db'
    return db

def exist_db():   #Func to be executed depending on existence.
    if os.path.exists("./db/user.db") is not True:
        init_db()
    if os.path.exists("./db/noticeboard.db") is not True:
        init_db_notice()    
    if os.path.exists("./db/noticeboard_re.db") is not True:
        init_db_notice_re() 
    if os.path.exists("./db/noticeboard_re2.db") is not True:
        init_db_notice_re2() 
    return ''
####################################################################################################################################
## Where to initalize and prepare the DB(database)
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

def init_db_notice_re2():
    with app.app_context():
        db = get_dbnotice_re2()
        f = open('noticeboard_re2.sql', 'r')
        db.execute(f.read())
        db.commit()
        db.close()
#########################################################################################################################
## Where is data manipulation language of notice board.
def search_board(text="", select=""):
    text = text.encode('utf-8')
    if select == "title":
        sql = 'SELECT * FROM notice_board WHERE title like "{}%" ORDER BY idx desc'.format(text)
    elif select == "writer": 
        sql = 'SELECT * FROM notice_board WHERE id="{}" ORDER BY idx desc'.format(text)
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
    #day = day.encode('utf-8')
    title=title.encode('utf-8')
    content = content.encode('utf-8')
    sql = 'INSERT INTO notice_board (id, title, content, day, files) VALUES ("{}","{}","{}","{}","{}")'.format(idid,title,content,day,files)
    db = get_dbnotice()
    db.execute(sql)
    db.commit()
    db.close()
    return ''

def get_noticedb_list():    
    sql = 'SELECT * FROM notice_board ORDER BY idx desc'#.format(idx_number)
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
    #day = day.encode('utf-8')
    title=title.encode('utf-8')
    content = content.encode('utf-8')
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
#########################################################################################################################
## Where is data manipulation language of notice board repple. 
def save_noticedb_re(readidx="", userid="", content="", day=""):     
     content = content.encode('utf-8')
     #day = day.encode('utf-8')
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

def update_noticedb_re(content="", idx=""):    
    content = content.encode('utf-8')
    db = get_dbnotice_re()    
    sql = 'UPDATE notice_board_re set content="{}" WHERE idx="{}"'.format(content, idx)
    rv = db.execute(sql)
    db.commit()
    db.close()
    return ''

def delete_noticedb_re(idx_1="", idx_2=""):
    db = get_dbnotice_re()
    sql = 'DELETE FROM notice_board_re where idx="{}" and originidx="{}"'.format(idx_1, idx_2)
    rv = db.execute(sql)
    db.commit()
    db.close()
    return ''
#########################################################################################################################
## Where is data manipulation language of USERS
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

def update_user(n_name=None, n_email=None, n_phone=None):
    if n_name is not None and n_email is not None and n_phone is not None:
       db = get_db()
       #r = get_user()
       print n_name
       print n_email
       print n_phone
       n_name = n_name.encode('utf-8')
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
#########################################################################################################################
## Where is Default Routing on the Homepage.

@app.route('/', methods=['GET', 'POST']) #Routing Default
def menetory():    
    if session.get('id') is not None:        
        return redirect(url_for('me_list'))
    return redirect(url_for('login')) 


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
            script_alert("welcome!") 
    return redirect(url_for('menetory'))

@app.route('/login')
def login():    
    if session.get('id') is not None:
        return redirect(url_for("menetory"))    
    return render_template('login.html', logon = menubar())    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    elif request.method == 'POST':
        in_new_id = request.form.get('new_id', '')
        in_new_pw = hash_224(request.form.get('new_pw', ''))
        in_new_name = request.form.get('new_name', '').encode('utf-8')
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

@app.route('/list', methods=['GET'])
def me_list():   
    res_list=[]
    board_re=[]    
    if request.args.get('category') is None and request.args.get('searchtext') is None:
        board_r = get_noticedb_list() 
    else:
        board_r=search_board(text=request.args.get('searchtext'), select=str(request.args.get('category')))
    for re_num in board_r:
        board_re.append(len(get_noticedb_list_re(re_num[0])))
    for x in range(len(board_r)):
        res_list.append(("",""))
        res_list[x] = ((board_r[x], board_re[x]))        
    return render_template('list.html', data = res_list, logon = menubar(), length = len(res_list))

 
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
    elif request.method == 'POST':
        ori_num=request.form.get('currentPage') #게시글 idx번호
        repple=request.form.get('commentContent')
        print ori_num
        print repple
        save_noticedb_re(readidx=ori_num, userid=session.get('id'), content=repple, day=day_date())
    return redirect(url_for('me_read', num=ori_num)) #"<script>history.go(-1);</script>" #redirect(url_for('me_read'))

@app.route('/rep_delete', methods=['GET', 'POST'])
def reupdate(): #, currentpage=None
    delnum=request.args.get('delnum')
    currentpage=request.args.get('currentpage')
    delete_noticedb_re(idx_1=delnum, idx_2=currentpage)
    script_alert("success repple delete")
    return redirect(url_for('me_read', num=currentpage))

@app.route('/repple_update', methods=['GET', 'POST'])
def reppleupdate(): #, currentpage=None
    if request.method == "POST":
        if request.form.get('pagenum'):
            content=request.form.get('re_content', 'nothing text')
            repple_idx=request.form.get('pagenum')
            update_noticedb_re(content=content, idx=repple_idx)            
            script_alert('success repple update')
            return redirect(url_for('me_read', num=request.form.get('currentPage')))
        return redirect(url_for('me_list'))

@app.route('/update', methods=['GET', 'POST'])
def me_update():    
    if request.method == "GET" and session.get('id') is not None:               
        r=get_noticedb_read(idx_number=request.args.get('num'))    
        return render_template('update.html', writerid=r[0][1], usertitle=r[0][2], usercontent=r[0][3], logon = menubar(), user=session.get('id'), textnum=r[0][0])
    elif request.method == "POST":          
        r=get_noticedb_read(idx_number=request.form.get('textnum'))   
        save_title=request.form.get('notitle')
        save_content=request.form.get('nocontent')
        
        file = request.files['_file']
        if allowed_file(file.filename) is False:
            res_filename = secure_filename(file.filename)
            file_path = './uploads/'+file.filename #+"."+filename.resplit('.')[1]           
            file.save(file_path)
        update_noticedb(idid=r[0][1], title=save_title,content=save_content, day=day_date(), files=file_path, idx=r[0][0])
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
    file_path=''
    if request.method == "GET":
        return render_template('write.html', userid=session.get('id'), logon = menubar())
    elif request.method == "POST":        
        writerid = session.get('id')
        save_title=request.form.get('notitle')
        save_content=request.form.get('nocontent')
        try:
            file = request.files['_file']
            pass
        except Exception as e:
            print e
        else:
            if allowed_file(file.filename) is False:
                res_filename = secure_filename(file.filename)
                file_path = './uploads/'+file.filename #+"."+filename.resplit('.')[1]           
                file.save(file_path)
        #send_from_diretory(app.config['UPLOAD_FOLDER'], filename)
        #save_files=request.form.get('_file')        
        save_noticedb(idid=writerid, title=save_title,content=save_content, day=day_date(), files=file_path)
        return redirect(url_for('me_list'))
    return ''

@app.route('/conversation', methods=['GET', 'POST'])
def conver():
    if request.method == "GET" and session.get('id') is not None:
        return render_template('conversation.html', logon = menubar())
    else:
        script_alert('Login is required.')       
        return redirect(url_for('/'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html', logon = menubar())

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', logon = menubar())

@app.errorhandler(404)
def page_not_found(e):
    return "<script>alert('잘못된 접근 입니다. 404');</script>" #return render_template('404.html'),404

@app.errorhandler(400)
def page_not_found(e):
    return "<script>alert('잘못된 접근 입니다. 400');</script>" #return render_template('404.html'),404

if __name__ == '__main__':
    exist_db()    
    # sioApp = socketio.Middleware(sio, app)    
    # el = eventlet.wsgi.server(eventlet.listen(('', 1111)), sioApp)
    # el.serve_forever()
    app.run(debug=True, host='0.0.0.0', port=1111)
    
