import os
import sys
from flask import Flask,render_template,request, make_response, flash
from pymongo import MongoClient
import base64

app = Flask(__name__)

client = MongoClient('###mongodburl###')
db=client['sarikadb']
collectionimg=db['images']


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        global uname
        uname=request.form['uname']
        passwd=request.form['pass']
        doc=db.userdetails.find({"username": uname})
        for i in doc:
            if i['password']==passwd:
                return render_template('index.html')
            else:
                return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method=='POST':
        file1 = request.files['file']
        comment=request.form['comment']
        fname=file1.filename
        content=file1.read()
        enc_cont=base64.b64encode(content)
        post={
            "username":uname,
            "filename":fname,
            "data":enc_cont,
            "comments":comment}
        collectionimg.insert(post)
        return render_template("index.html")
    
@app.route('/list', methods=['GET', 'POST'])
def listimg():
    if request.method=='POST':
        doc=collectionimg.find({"username": uname})
        return_string = ""
        for i in doc:
            data=i['data']
            usname=i['username']
            comments=i['comments']
            flname=i['filename']
            pic_data = "data:image/jpeg;base64," + data

        return pic_data
    
@app.route('/listall', methods=['GET', 'POST'])
def listallimg():
    if request.method=='POST':
        doc=collectionimg.find({})
        return_string = ""
        for i in doc:
            data=i['data']
            usname=i['username']
            comments=i['comments']
            flname=i['filename']
            pic_data = "data:image/jpeg;base64," + data
		return pic_data
 
@app.route('/deleteall', methods=['GET', 'POST'])
def deleteallimg():
    if request.method=='POST': 
        collectionimg.remove({"username": uname})
        return "Deleted all images"
    

        

if __name__ == "__main__":
    app.run(debug=True)
    
    
#References:
#http://api.mongodb.com/python/current/tutorial.html
#https://docs.python.org/2/library/base64.html
#http://stackoverflow.com/questions/8499633/how-to-display-base64-images-in-html
