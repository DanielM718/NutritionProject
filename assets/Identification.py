from lib2to3.pytree import convert
from flask import Flask, request, make_response, jsonify, Response, render_template
from flask_cors import CORS
from http import cookies as Cookie
import cv2
import numpy as np
import requests
import json

camera = cv2.VideoCapture(0)
app = Flask(__name__)

siteURL = "https://api.foodai.org/v4.1/classify"
url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=XnRtjuAtuUfz6a43IFDUyLbcwdDJcUhkpRGKbY9N"

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

    for responseFood in responseFoods:
        nutrients = responseFood['foodNutrients']

        for nutrient in nutrients:
            caloriesKCAL = nutrient['nutrientId'][1008]['value']
            caloriesKj = nutrient['nutrientId'][1062]['value']
            calories = caloriesKCAL + caloriesKj
    
    print(calories)
        




@app.route('/')
def main():
    return render_template('Vid.html')

@app.route('/testingRoute', methods=['POST', 'GET'])
def test():
    if request.method == 'GET':
        return render_template('Vid.html')
    else:
        print('proccesing frame') 
        classifier(getFrame())
        return render_template('Vid.html')

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')            

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')