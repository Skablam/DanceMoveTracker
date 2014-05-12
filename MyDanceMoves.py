import os

from flask import Flask, render_template, session
from flask.ext.assets import Environment, Bundle
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

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
    return render_template('/welcome.html')

@app.route("/movelist")
def movelist():
    return render_template('/move_list.html')

@app.route("/login")
def login():
    return render_template('/login.html')  

@app.route("/register")
def register():
    return render_template('/register.html')   

@app.route("/about")
def about():
    return render_template('/about.html')  

@app.route("/contact")
def contact():
    return render_template('/contact.html')  


if __name__ == "__main__":
    app.run(host="0.0.0.0")