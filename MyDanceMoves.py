from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)


# Static assets
assets = Environment(app)
css_main = Bundle(
    'stylesheets/main.scss',
    filters='scss',
    output='build/stylesheets/main.css',
    depends="**/*.scss"
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")