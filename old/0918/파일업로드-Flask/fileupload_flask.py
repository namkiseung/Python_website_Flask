# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, url_for
from werkzeug import secure_filename

app = Flask(__name__)
@app.route('/upload')
def upload_render():
    return render_template('/upload.html')

@app.route('/fileUpload', methods=['POST'])
def upload_file():
    f = request.files['_file']
    # Directory + filename
    f.save('./uploads/' + secure_filename(f.filename))
    return 'uploads 디렉터리 -> 파일 업로드 성공!'

@app.route('/<number>')
@app.route('/<int:number>')
@app.route('/<float:number>')
def index(number):
    return 'a' #redirect(url_for('upload'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1111)
