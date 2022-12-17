from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user_model import User
# from flask_app.models.movie_model import Movie
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt (app)

import os
import requests
import json



@app.route('/home')
def home():
    if 'user_id' not in session: 
        flash(" You must login before you can access the website.")
        # need to add jinja in html
        return redirect('/')
    data = {
        'id': session['user_id']
    }

    # start of API code

    url = "https://moviesdatabase.p.rapidapi.com/titles/x/upcoming"
    
    headers = {
        "X-RapidAPI-Key": os.environ['API_KEY'],
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    api_data =json.loads(response.text)
    # pulls data from api
    # parses the data into a JSON format

    for titles in api_data:
        print(titles)
        # prints out page, next, entries, results twice
    for titles in api_data:
        print(titles["entries"]['textType'])

    return render_template("home.html", user = User.get_by_id(data))






















@app.route('/')
def index():
    return render_template('index.html')

# Register User
@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "username": request.form['username'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/home')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/home')




@app.route('/profile')
def profile():
    if 'user_id' not in session: 
        flash(" You must login before you can access the website.")
        # need to add jinja in html
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template("profile_page.html", user = User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear
    return redirect('/')

@app.route('/movie')
def movie():
    return render_template("movie.html")
