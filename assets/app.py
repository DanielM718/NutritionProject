#test to make sure Joseph N has connected to repository
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)

#still troubleshooting, app wont launch on my end