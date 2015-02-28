from flask.ext.security import UserMixin, RoleMixin
from application import db

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    moves = db.relationship('Move', backref=db.backref('moves'))
    lessons = db.relationship('Lesson', backref=db.backref('lessons'))

class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movename = db.Column(db.String(100))
    category = db.Column(db.String(50))
    movetags = db.Column(db.String(255))
    video_link = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_link = db.Column(db.String(255))
    teachers = db.Column(db.String(255))
    date = db.Column(db.String(100))
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
