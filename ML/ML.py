from flask import Flask, render_template, request, json, jsonify, current_app as app
from datetime import date
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 0

@app.route('/test', methods=['POST'])
def api():
    return 0


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')