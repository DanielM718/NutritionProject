from email.message import EmailMessage
from re import template
from flask import Flask, render_template, request, current_app as app 
from flask_cors import CORS
import requests
import sqlite3
import sys
import os
import firebase_admin
from firebase_admin import credentials, firestore



cred = credentials.Certificate('nutrition-app-ba2a6-firebase-adminsdk-419j0-3336f9c6a5.json')
firebase_admin.initialize_app(cred)
db = firestore.client()



class Sign_up:
    def ___init__(self,email, username, password):
        self.email = email
        self.username = username
        self.password = password

        #initilize all parameters

        


app = Flask(__name__)

CORS(app, resources=r'/api/*')

@app.route('/')
def main():

    return render_template('index.html')

@app.route('/api/sign_up_page', methods=['GET','POST'])
def sign_up_page():
    eml = request.form['email']
    user_n=request.form['username']
    passwrd=request.form['password']
    #request info from form

    def user_dict():
        return {'email':eml,
                'username':user_n,
                'password': passwrd

    }
    username = db.collection('user_info')#access user_info collection
    user = username.document(user_n).set(user_dict())#adds data passed to firebase DB
    
    #login_username= request.form['']
    #login_password= request.form['']
    

    #if sign_up.email == eml and sign_up.username == user_n and sign_up.password == passwrd:
    return render_template('list.html', eml=eml,user_n=user_n, passwrd =passwrd)


    
    #return render_template('index.html', username=username, user=user)


@app.route('/login',methods=['GET','POST'])
def login():
    #  login_username= request.form['login_username']
    #  login_password= request.form['login_password']

    #  if db.username == login_username and db.password== login_password:
    #     return render_template('test.html',login_username = login_username, login_password=login_password)
    #  else:
        return render_template('login.html')
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')