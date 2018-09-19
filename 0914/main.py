from flask import Flask, g, request, render_template, session
import sqlite3, hashlib

app=Flask(__name__)
DATABASE='./db/test.db'
app.secret_key = 'abcde'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db=get_db()
        with open('schema.sql', 'r') as f:
            db.execute(f.read())
            db.commit()
            db.close()
    return ''

def save_user(save_id='',save_pw='', save_email=''):
    sql='INSERT INTO users VALUES ("{}", "{}", "{}")'.format(save_id, save_pw, save_email)
    db = get_db()
    res=db.execute(sql)
    db.commit()
    db.close()

def get_info_db():
    sql = 'SELECT * FROM users'
    db = get_db()
    res = db.execute(sql)
    res_res = res.fetchall()
    print '#####res_res value : ',res_res
    return res_res

def get_user(userid=''):
    sql = 'SELECT email FROM users WHERE id="{}"'.format(userid)
    db = get_db()
    res = db.execute(sql)
    get_result = res.fetchall()
    print(get_result)
    print(type(get_result))
    print(dir(get_result))
    if get_result is None:
        return None
    else:
        return get_result
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        r_id = request.form.get('user_id', '')
        r_pw = request.form.get('user_pw', '')
        session['user_id']=r_id
        print type(get_user(userid=r_id))
        if session['user_id'] is not None:
            return render_template('home.html', present=get_user(userid=session['user_id']))
        #return render_template('login.html', select_data=get_info_db(), data1=r_id, data2=r_pw)
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
       return render_template('register.html')
    else:
       regis_id = request.form.get('hi_id','')
       tmp_regis_pw = request.form.get('hi_pw','')
       regis_pw = hashlib.sha224(tmp_regis_pw).hexdigest()
       print 'hex age : '+tmp_regis_pw
       print 'hex after : '+regis_pw
       regis_em = request.form.get('hi_email','')
       save_user(save_id=regis_id, save_pw=regis_pw, save_email=regis_em)
       return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return render_template('login.html')

if __name__=="__main__":
    #init_db()
    app.run(debug=True, host="0.0.0.0", port=1111)
