#test to make sure Joseph N has connected to repository

from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

#still troubleshooting, app wont launch on my end