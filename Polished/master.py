from email.message import EmailMessage
from lib2to3.pytree import convert
from re import template
from flask import Flask, render_template, request,redirect, Response, jsonify, make_response, current_app as app 
from flask_cors import CORS
import requests
import json
import sqlite3
import sys
import os
import cv2
import firebase_admin
from firebase_admin import credentials, firestore

camera = cv2.VideoCapture(0)

siteURL = "https://api.foodai.org/v4.1/classify"
url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=XnRtjuAtuUfz6a43IFDUyLbcwdDJcUhkpRGKbY9N"


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
def gen_frames():
    # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
def getFrame():
        ret, frame = camera.read()
        if ret:
            cv2.imshow('frame',frame)
            return cv2.imencode(".jpeg",frame)[1].tobytes()  
def classifier(binaryImage):
    data = {
        'image_data': ("banana.png", binaryImage),
        'num_tag': (None, "4"),
        'api_key': (None, 'a1e3760442d8a4125ad5a8f51542537bc0de167d')
    }

    response = requests.Request('POST',siteURL,files=data)
    res = response.prepare()
    session = requests.Session()
    result = session.send(res)
    raw = result.text
    convert = json.loads(raw)
    Food = convert['food_results'][0][0]
    print(Food)

    payload = json.dumps({
        "query": Food
    })
    headers = {
        'Content-Type': 'application/json'
    }

    responseFoodRaw = requests.request("POST", url, headers=headers, data=payload)
    responseFoodUnPackaged = responseFoodRaw.text
    foodConversion =  json.loads(responseFoodUnPackaged)
    responseFoods = foodConversion['foods']

    i = 0
    brand = 0
    h=0
    Kcal = []
    # Kjoules = []

    while brand < len(responseFoods):
        nutrients = responseFoods[brand]['foodNutrients']
        for i in nutrients:
            if i['nutrientId'] == 1008:
                Kcal.append(i['value'])
            elif i['nutrientId'] == 1062:
                conversion = (i['value'])/(4.184)
                Kcal.append(conversion)
        brand+=1 
    # for cal in Kcal:
    #     print(cal)

    Calories = round((sum(Kcal))/(len(Kcal)))
     
    # for calk in Kjoules:
    #     print(calk)
    return Food, Calories


app = Flask(__name__)

CORS(app, resources=r'/api/*')

@app.route('/')
def main():
    calories = 0
    return render_template('vid.html', calories = calories)

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


@app.route('/graph')
def graph():
    data=[
        ('chips',180),
        ('Chicken taco\'s', 490),
        ('rice',233)
    ]
    x_axis=[row[0]for row in data]
    y_axis=[row[0]for row in data]

    return render_template('graph.html',data=data, x_axis=x_axis,y_axis=y_axis)


@app.route('/testingRoute', methods=['POST', 'GET'])
def test():
    if request.method == 'GET':
        return render_template('Vid.html')
    else:
        print('proccesing frame') 
        calories = classifier(getFrame())
        print(calories)
        return render_template('Vid.html', calories=calories)

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') 
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')