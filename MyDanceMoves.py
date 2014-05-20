import os
import json
import requests
from flask import Flask, render_template, session, request, flash
from flask.ext.assets import Environment, Bundle
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.bcrypt import Bcrypt
from models import User

app = Flask(__name__)
bcrypt = Bcrypt(app)

if os.environ.get('DEBUG_ON', None) == 'False':
	app.debug=False
else:
	app.debug=True

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

@app.route("/")
def index():
    return render_template('welcome.html')

@app.route("/movelist")
def movelist():
    return render_template('move_list.html')

@app.route("/lessonlist")
def lessonlist():
    return render_template('lesson_list.html')

@app.route("/addmove")
def addmove():
    return render_template('add_move.html')

@app.route("/login")
def login():
    return render_template('login.html')  

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        newuser = register_user(request.form.get('username'),
                             request.form.get('password'),
                             request.form.get('email'))
        if newuser:
            flash('Registration successful.')
            return redirect('/')
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
    newuser = User()
    newuser.name = username
    newuser.email = email
    
    pw_hash = bcrypt.generate_password_hash(password)
    newuser.password_hash = pw_hash

    payload = json.dumps(vars(newuser))

    r = requests.post("localhost:8081/registeruser", params=payload)

    return newuser

if __name__ == "__main__":
    app.run(host="0.0.0.0")