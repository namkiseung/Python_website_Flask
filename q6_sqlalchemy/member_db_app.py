from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/member.db'
db = SQLAlchemy(app)

class User(db.Model):
   __tablename__ = 'users'
   idx = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(40), unique=True, nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   phone = db.Column(db.String(14), unique=True)
   password = db.Column(db.String(255), nullable=False)
   avator = db.Column(db.String(100))
   grade = db.Column(db.Integer, nullable=False)
   
   def __init__(self, username, email, phone, password, avator, grade):
      self.username = username.encode('utf-8')
      self.email = email
      self.phone = phone
      password = "{}".format(password)
      hash_pass = pbkdf2_sha256.hash(password)
      self.password = hash_pass
      self.grade = grade
      self.avator = avator

   def __repr__(self):
      return '<User %r>' % self.username

def verify_login(_username='', _password=''):
   _user = User.query.filter(User.username == _username).first()
   return pbkdf2_sha256.verify(_password, _user.password)

def user_add(username, email, phone, password, avator='', grade=0):
   _user = User(username, email, phone, password, avator, grade)
   #print "This is func 'user_add()'"
   #print _user.username
   #print _user.email
   #print _user.phone
   #print _user.grade
   #print _user.avator
   #print _user.password 
   db.session.add(_user)
   db.session.commit()

def user_update(username, email, phone, password, avator='', grade=0):
   _user = User.query.filter(User.username == username).first()
   _user.email = email
   _user.username = username
   _user.phone = phone
   _user.avator = avator
   _user.grade = grade 
   #print "This is func 'user_update()'"
   #print "print _user_ : {}" % _user
   #print _user.email
   #print _user.username
   #print _user.phone
   #print _user.grade
   #print _user.avator
   db.session.add(_user)
   db.session.commit()

def user_delete(username):
   _user = User.query.filter(User.username == username).first()
   #print "This is func 'user_delete()'"
   #print "print _user_ : {}" % _user
   db.session.delete(_user)
   db.session.commit()

if __name__=='__main__':
   db.create_all()   

