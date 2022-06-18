
from flask import Flask, render_template, app 
import cv2
#jsonify, request, make_response, abort 
camera = cv2.VideoCapture(0)

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


app = Flask(__name__)
@app.route('/')
def start():
    return "Welcome to our project"

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/video_feed')
def video_feed():
        #Video streaming route. Put this in the src attribute of an img tag
    return Response (gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
