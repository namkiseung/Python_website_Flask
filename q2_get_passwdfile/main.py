from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
   f = open('/etc/passwd', 'r')
   list_a=[]
   for x in f.readlines():
      list_a.append(x)
   return render_template('etc_passwd_file.html', data=list_a)

if __name__=="__main__":
  app.run(debug=True, host='0.0.0.0', port=1111)

