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
def info():
    email=db.document('user_info').get('password')
    password= db.document('user_info').get('password')
    username=db.document('user_info').get('username')
    info_dict={'email':email,
    'password':password,
    'username':username,

    }
        


app = Flask(__name__)

CORS(app, resources=r'/api/*')

@app.route('/')
def main():

    return render_template('index.html')

@app.route('/api/sign_up_page', methods=['GET','POST'])
def sign_up_page():
    if request.method=='POST':
        eml = request.form['email']
        user_n=request.form['username']
        passwrd=request.form['password']
    else:
        pass
    #request info from form
    def user_dict():
        return {'email':eml,
                'username':user_n,
                'password': passwrd

    }
    

    #user_data = db.collection('').document(user.username).get().to_dict()
    username = db.collection('user_info')#access user_info collection
    user = username.document(user_n).set(user_dict())
    
    return render_template('list.html', eml=eml,user_n=user_n, passwrd =passwrd,username=username,user=user)
        



@app.route('/personal' , methods=['GET','POST'])
def personal():
    username = db.collection('user_info')
    username_str=str(username)
    user = username.document('user_info').get()
    
    
    return render_template('personal.html', username=username,user=user,username_str=username_str)


@app.route('/login',methods=['GET','POST'])
def login():
  login_username = request.form['username']
  login_password = request.form['password']
  if request.method == 'POST':
      login_username = request.form['username']
      login_password = request.form['password']
      
  else:
      pass
  def just_dict():
      return{
          'username':login_username,
          'password':login_password,
      }
  
  
  username = db.collection('user_info')#access user_info collection
  name=username.document(login_username).set(just_dict())

    
  return  just_dict()#render_template('personal.html',login_username=login_username,login_password=login_password) just_dict()  
    
    
     
    # if login_form and login_form_p == check:
    #     return render_template('login.html', check=check, login_form=login_form, login_form_p=login_form_p)
    # else:
    #     return check

        


   
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')