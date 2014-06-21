import os
import json
import requests
from flask import Flask, render_template, session, request, redirect, flash, g, send_from_directory
from flask.ext.assets import Environment, Bundle
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required, UserMixin
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.bcrypt import Bcrypt
from models import User

app = Flask(__name__)

#hashing package
bcrypt = Bcrypt(app)

#login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Read environment variables
if os.environ.get('DEBUG_ON', None) == 'False':
    app.debug=False
else:
    app.debug=True  

MyDanceMoves_Service = os.environ.get('MyDanceMoves_Service', None)

app.config['SECRET_KEY'] = os.urandom(24)

#toolbar = DebugToolbarExtension(app)

# Static assets
assets = Environment(app)
css_main = Bundle(
    'stylesheets/main.scss',
    filters='scss',
    output='build/stylesheets/main.css',
    depends="stylesheets/views/*.scss"
)
assets.register('css_main', css_main)

@login_manager.user_loader
def load_user(username):
    resp = requests.get(MyDanceMoves_Service + "/getuser/" + username).json()  
    user_to_load = User(username, resp["User"]["Password"])
    user_to_load.email = resp["User"]["Email"]
    return user_to_load

def check_user(username, password):
    print os.environ.get('MyDanceMoves_Service')
    resp = requests.get(MyDanceMoves_Service + "/getuser/" + username).json() 
    result = resp["Result"] 
    if result == "user found":
        password_hash = resp["User"]["Password"] 
        if bcrypt.check_password_hash(password_hash, password):
            registered_user = User(username, password)
            return registered_user    
    else:
        return None

@app.before_request
def before_request():
    g.user = current_user

@app.route("/")
def index():
    return render_template('welcome.html')

@app.route("/movelist")
@login_required
def movelist():
    payload = {"username" : g.user.id}
    resp = requests.get(MyDanceMoves_Service + "/movelist", params=payload)    
    move_list = resp.json()["Moves"]

    return render_template('move_list.html', move_list=move_list)

@app.route("/lessonlist")
@login_required
def lessonlist(): 
    return render_template('lesson_list.html')

@app.route("/addmove", methods=['GET', 'POST'])
def addmove():
    if request.method == 'GET':
        return render_template('add_move.html')   
    movename = request.form.get('movename')
    category = request.form.get('category')
    tags = request.form.get('movetags')
    video_link = request.form.get('videolink') 

    payload = json.dumps({'name' : movename, 'category' : category, 'tags' : tags, 'video_link' : video_link, 'username' : g.user.id})
    header = {'content-type': 'application/json'}

    print payload
    print header

    r = requests.post(MyDanceMoves_Service + "/move", data=payload, headers=header)
    return redirect('/movelist') 

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    registered_user = check_user(username, password)
    if registered_user == None:
        flash('Username or Password is invalid' , 'error')
        return redirect('/login')    
    login_user(registered_user)
    return redirect('/') 

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        newuser = register_user(request.form.get('username'),
                             request.form.get('password'),
                             request.form.get('email'))
        if newuser:
            flash("Registration successful!")
            return redirect('/login')
        else:
            error = 'Failed to register user. Try another username.'
    return render_template('register.html')   

@app.route("/about")
def about():
    return render_template('about.html')  

@app.route("/contact")
def contact():
    return render_template('contact.html')  


def register_user(username, password, email):
    newuser = User(username, "")
    
    pw_hash = bcrypt.generate_password_hash(password)
    newuser.password = pw_hash
    newuser.email = email

    payload = json.dumps(vars(newuser))

    print payload

    header = {'content-type': 'application/json'}

    r = requests.post(MyDanceMoves_Service + "/registeruser", data=payload, headers=header)

    return newuser

if __name__ == "__main__":
    app.run(host="0.0.0.0")