from re import template
from flask import Flask, render_template, request, current_app as app 
from flask_cors import CORS
import requests
import sqlite3
import sys
import os
import firebase_admin
from firebase_admin import credentials, firestore



cred = credentials.Certificate('/home/pi/Desktop/nutrition-backend/static/data')
firebase_admin.initialize_app(cred)
db = firestore.client()





config={
    "apiKey": "AIzaSyABd1dfgnJlVAX6fmjH2N_wxXNuM30CFko",
  "authDomain": "nutrition-app-ba2a6.firebaseapp.com",
  "projectId": "nutrition-app-ba2a6",
  "storageBucket": "nutrition-app-ba2a6.appspot.com",
  "messagingSenderId": "738081012918",
  "appId": "1:738081012918:web:2010dcf255f4eb9bed3a17",
  "measurementId": "G-8345LGWE3T"
}



app = Flask(__name__)

CORS(app)

@app.route('/sign-Up')
def main():

    return render_template('index.html')

@app.route('/api/user_login', method=["GET"])
def get():
    username = db.collection('user_info')
    user= username.document("lgjRVl3YSppicOUbjZNd").get()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')