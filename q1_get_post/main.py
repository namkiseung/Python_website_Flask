from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'GET':
      args=request.args.get('name', '')
      return render_template('exam_get.html', data=args)
   else:      
      a1=request.form.get('last_name')
      a2=request.form.get('first_name') 
      return render_template('exam_get.html', name1=a1, name2=a2 )

if __name__=="__main__":
  app.run(debug=True, port=1111, host='0.0.0.0')

