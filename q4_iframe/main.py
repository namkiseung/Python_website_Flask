from flask import Flask, request

app=Flask(__name__)

@app.route('/', methods=['GET'])
def index(inputcase=''):
   if request.method == 'GET':
      if request.args.get('inputcase') is not '':
         url_name = request.args.get('inputcase')
	 print url_name
         str = '<iframe src="http://www.{}.com">{}'.format(url_name, url_name)
         print str
         return str
   return 'Nothing'

if __name__=="__main__":
   app.run(debug=True, host='0.0.0.0', port=1111)
