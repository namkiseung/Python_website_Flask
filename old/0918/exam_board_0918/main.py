# -*- coding:utf-8 -*-
from flask import Flask, g, request, render_template
app=Flask(__name__)

@app.route('/')
def index():
   return render_template('list.html')

@app.route('/b')
def index2():
   return render_template('read.html')

@app.route('/c')
def index3():
   return render_template('write.html')
  

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=1111)
