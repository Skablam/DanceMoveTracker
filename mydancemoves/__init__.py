import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)

app.config.from_object(os.environ.get('SETTINGS'))

db = SQLAlchemy(app)

# Static assets
assets = Environment(app)
css_main = Bundle(
    'stylesheets/main.scss',
    filters='scss',
    output='build/stylesheets/main.css',
    depends="stylesheets/views/*.scss"
)
assets.register('css_main', css_main)
