from email.message import EmailMessage
from re import template
from flask import Flask, render_template, request,redirect, current_app as app 
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
        



@app.route('/personal' , methods=['GET','POST'])
def personal():
    username = db.collection('user_info')
    username_str=str(username)
    user = username.document('user_info').get()
    
    var='hello'
    return render_template('personal.html',var=var, username=username,user=user,username_str=username_str)


@app.route('/login',methods=['GET','POST'])
def login():
    login_form = request.form.get('username')
    login_form_p= request.form.get('password')
    

    def login_dict():
        return{
            "username":login_form,
            "password":login_form_p
        }
    
    return render_template('login.html', login_form =login_form,login_form_p=login_form_p)  and login_dict()
    #response=redirect('/login')
    # check=db.collection('user_info').document('username').get()
    # print(check)
     
    # if login_form and login_form_p == check:
    #     return render_template('login.html', check=check, login_form=login_form, login_form_p=login_form_p)
    # else:

        


   
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')