from flask import Flask, request, make_response, jsonify, Response, render_template
from flask_cors import CORS
from http import cookies as Cookie
import cv2

camera = cv2.VideoCapture(0)
app = Flask(__name__)


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

@app.route('/')
def main():
    return render_template('Vid.html')

@app.route('/testingRoute', methods=['POST', 'GET'])
def test():
    if request.method == 'GET':
        return render_template('Vid.html')
    else:
        print('proccesing frame') 
        return render_template('Vid.html')

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')            

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')