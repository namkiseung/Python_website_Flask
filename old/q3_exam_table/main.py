from flask import Flask, render_template, g, request
import sqlite3
DATABASE='./db/test.db'
app=Flask(__name__)

def get_db():
   db = getattr(g, '_database', None)
   if db is None:
      db = g._database = sqlite3.connect(DATABASE)
      db.row_factory = sqlite3.Row
      return db

def init_db():
    with app.app_context():
         db=get_db()
         with open('schema.sql', 'r') as f:
              db.cursor().executescript(f.read())
              db.commit()
def add_stu(name='', classs=0, age=0):
    sql = "INSERT INTO students (name, class, age) VALUES ('{}','{}','{}')".format(name, classs, age)
    db=get_db()
    db.execute(sql)
    db.commit()
    return ''

def list_select():
    sql = "SELECT * FROM students"
    db = get_db()
    rv = db.execute(sql)
    result = rv.fetchall() 
    return result

@app.route('/', methods=['GET','POST'])
def index():
   if request.method == 'GET':
       info = list_select()
       return render_template('stu_save_list.html', data=info)
   else:
       add_stu(name=request.form.get('name'), classs=request.form.get('class'), age=request.form.get('age'))       
       return render_template('stu_save_list.html')


   return 'a'

if __name__=="__main__":
  #init_db()
  app.run(debug=True, host='0.0.0.0', port=1111)
