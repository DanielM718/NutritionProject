
from flask import Flask, render_template, app, cv2, jsonify, request, make_response, abort 




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

@app.route('')

if __name__ == "__main__":
    app.run(debug=True)
