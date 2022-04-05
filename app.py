from re import template
from flask import Flask, render_template, request, current_app as app 
from flask_cors import CORS
import requests
import sqlite3
import sys
import os
import firebase_admin
from firebase_admin import credentials, firestore



cred = credentials.Certificate('nutrition-app-ba2a6-firebase-adminsdk-419j0-8a54f8eead.json')
firebase_admin.initialize_app(cred)
db = firestore.client()



class sign_up:
    def ___init__(self,email, username, password):
        self.email = email
        self.username = username
        self.password = password

        

        signUp = sign_up(email,username,password)


app = Flask(__name__)

CORS(app, resources=r'/api/*')

@app.route('/')
def main():

    return render_template('index.html')

@app.route('/api/sign_up_page', methods=['GET','POST'])
def sign_up_page():
    username = db.collection('user_info')#access user_info collection
    user = username.document("lgjRVl3YSppicOUbjZNd").get()#gets username
    eml = request.form['email']
    user_n=request.form['username']
    passwrd=request.form['password']
    #login_username= request.form['']
    #login_password= request.form['']
    info_list={'email':eml,
                'username':user_n,
                'password': passwrd

    }

    #if sign_up.email == eml and sign_up.username == user_n and sign_up.password == passwrd:
    return render_template('list.html', eml=eml,user_n=user_n, passwrd =passwrd, info_list=info_list)


    
    #return render_template('index.html', username=username, user=user)


@app.route('/api/login', methods=['GET','POST'])
def login():
    if signUp.username == request.form['username'] and signUp.password == request.form['password']:
        return render_template('login.html')
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')