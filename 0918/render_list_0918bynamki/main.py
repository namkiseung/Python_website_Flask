# -*- coding:utf-8 -*-
from flask import Flask, g, request, render_template
import requests
from bs4 import BeautifulSoup

app=Flask(__name__)

@app.route('/')
def index():
   #req = requests.get("https://github.com/explore")
   req = requests.get("https://www.naver.com/")
   html = req.text
   soup = BeautifulSoup(html, 'html.parser')
   list_text=[]
   for tag in soup.select('span[class="ah_k"]'):
       print tag.text
       list_text.append(tag.text)
   return render_template('index.html', data=list_text)
  
@app.route('/github')
def github():
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
   return render_template('index2.html', data=result)

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=1111)
