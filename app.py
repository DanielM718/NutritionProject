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

    #user_data = db.collection('').document(user.username).get().to_dict()
    username = db.collection('user_info')#access user_info collection
    user = username.document(user_n).set(user_dict())#adds data passed to firebase DB
    #user_g = db.collection('user_info').document(user.user_n).get().user_dict()
    #login_username= request.form['']
    #login_password= request.form['']
    
    #if eml and user_n and passwrd == user_g:
        #return '<h2> true</h2>'

        #if email.request and password.requestform == user_dict()
        #----------- fix return of dictionary to work with class to allow global access----------
    
    return render_template('list.html', eml=eml,user_n=user_n, passwrd =passwrd)
        

    
    


@app.route('/login',methods=['GET','POST'])
def login():
    login_form= request.form['username']
    login_form_p= request.form['password']

    check=db.document('user_info').get()
     
    if login_form and login_form_p == check:
        return True
    else:
        return render_template('/login.html')
         
   
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')