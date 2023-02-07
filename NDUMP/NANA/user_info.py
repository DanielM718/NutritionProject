import requests
from flask import redirect, request
class check_form:
        if request.method=='POST':
            eml= request.form['email']
            login_form = request.form['username']
            login_form_p= request.form['password'] 
        else:
            redirect('/')



    
