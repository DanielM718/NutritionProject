#test to make sure Joseph N has connected to repository
from flask import Flask, render_template, app



app = Flask(__name__)
@app.route('/')
def start():
    return "Welcome to our project"

@app.route('/about')
def about():
    return render_template('about.html', title='About - Nutrition Project')

@app.route('/login')
def login():
   return render_template('login.html', title='Login - Nutrition Project')

@app.route('/home')
def home():
    return render_template('home.html', title='Home - Nutrition Project')

if __name__ == "__main__":
    app.run(debug=True)

#still troubleshooting, app wont launch on my end