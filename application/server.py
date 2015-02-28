import os
import json
import requests
import bcrypt
from application import app, db
from flask import render_template, session, request, redirect, flash, g, send_from_directory
from flask.ext.security import login_required, current_user, Security, SQLAlchemyUserDatastore
from flask.ext.security.utils import *
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Role, Move, Lesson

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

app.config['SECRET_KEY'] = os.urandom(24)

# if app.debug:
#   toolbar = DebugToolbarExtension(app)

@app.before_request
def before_request():
    g.user = current_user

@app.route("/")
def index():
    return render_template('welcome.html')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/movelist")
@login_required
def movelist():
    move_list = Move.query.filter_by(user_id=g.user.id).all()

    return render_template('move_list.html', move_list=move_list)

@app.route("/lessonlist")
@login_required
def lessonlist():
    lesson_list = Lesson.query.filter_by(user_id=g.user.id).all()

    return render_template('lesson_list.html', lesson_list=lesson_list)

@app.route("/addmove", methods=['GET', 'POST'])
@login_required
def addmove():
    if request.method == 'GET':
        return render_template('add_move.html')

    newmove = Move()

    newmove.movename = request.form.get('movename')
    newmove.category = request.form.get('category')
    newmove.movetags = request.form.get('movetags')
    newmove.video_link = request.form.get('videolink')
    newmove.user_id = g.user.id

    g.user.moves.append(newmove)

    db.session.add(newmove)
    db.session.add(g.user)
    db.session.commit()

    return redirect('/movelist')

@app.route("/addlesson", methods=['GET', 'POST'])
@login_required
def addlesson():
    if request.method == 'GET':
        return render_template('add_lesson.html')

    newlesson = Lesson()

    newlesson.date = request.form.get('lessondate')
    newlesson.category = request.form.get('category')
    newlesson.teachers = request.form.get('lessonteachers')
    newlesson.video_link = request.form.get('videolink')
    newlesson.user_id = g.user.id

    g.user.lessons.append(newlesson)

    db.session.add(newlesson)
    db.session.add(g.user)
    db.session.commit()

    return redirect('/lessonlist')

@app.route("/editmove/<id>", methods=['GET', 'POST'])
@login_required
def editmove(id):

  existingmove = Move.query.filter_by(id=id).first()

  if request.method == 'GET':
      return render_template('edit_move.html', Move=existingmove)

  existingmove.movename = request.form.get('movename')
  existingmove.category = request.form.get('category')
  existingmove.movetags = request.form.get('movetags')
  existingmove.video_link = request.form.get('videolink')

  db.session.add(existingmove)
  db.session.commit()

  return redirect('/movelist')

@app.route("/editlesson/<id>", methods=['GET', 'POST'])
@login_required
def editlesson(id):

  existinglesson = Lesson.query.filter_by(id=id).first()

  if request.method == 'GET':
      return render_template('edit_lesson.html', lesson=existinglesson)

  existinglesson.date = request.form.get('lessondate')
  existinglesson.category = request.form.get('category')
  existinglesson.teachers = request.form.get('lessonteachers')
  existinglesson.video_link = request.form.get('videolink')

  db.session.add(existinglesson)
  db.session.commit()

  return redirect('/lessonlist')

@app.route("/deletemove/<id>", methods=['GET', 'POST'])
@login_required
def deletemove(id):

  existingmove = Move.query.filter_by(id=id).first()

  db.session.delete(existingmove)
  db.session.commit()

  return redirect('/movelist')

@app.route("/deletelesson/<id>", methods=['GET', 'POST'])
@login_required
def deletelesson(id):

  existinglesson = Lesson.query.filter_by(id=id).first()

  db.session.delete(existinglesson)
  db.session.commit()

  return redirect('/lessonlist')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')
