 #!/usr/bin/python
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories,Courses
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.orm import scoped_session

from flask import session as login_session
import random
import string

import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


APPLICATION_NAME = "Restaurant Menu Application"



engine = create_engine('sqlite:///restaurantmenu.db',
                poolclass=SingletonThreadPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)





@app.route('/categories/<int:category_id>/courses/JSON')
def coursesJSON(category_id):
   courses=session.query(Courses).filter_by(category_id=category_id).all()
   return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/JSON')
@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Categories).all()
    courses=session.query(Courses).all()
    return jsonify(categories=[r.serialize for r in categories])


@app.route('/')
@app.route('/categories/')
def show_categories():
	categories = session.query(Categories).all()
	courses=session.query(Courses).all()
	return render_template('categories.html', categories=categories,courses=courses)
	
@app.route('/categories/new/', methods=['GET', 'POST'])
def new_category():
	if request.method == 'POST':
		new_category=Categories(name=request.form['name'])
		session.add(new_category)
		session.commit()
		return redirect(url_for('show_categories'))
	else:
		return render_template('new_category.html')
	
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def edit_category(category_id):
	edited_category = session.query(Categories).filter_by(id=category_id).one()
	if request.method == 'POST':
		if request.form['name']:
			edited_category.name=request.form['name']
			session.add(edited_category)
			session.commit()
			return redirect(url_for('show_categories'))
	else:
		return render_template('edit_category.html', category=edited_category)
	
@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
	deleted_category = session.query(Categories).filter_by(id=category_id).one()
	if request.method == 'POST':
		session.delete(deleted_category)
		session.commit()
		return redirect(url_for('show_categories'))
	else:
		return render_template('delete_category.html', category=deleted_category)	


@app.route('/categories/<int:category_id>/courses/')
def show_courses(category_id):
	categories = session.query(Categories).all()
	courses=session.query(Courses).filter_by(category_id=category_id).all()
	return render_template('show_courses.html', courses=courses, categories=categories,category_id=category_id)


@app.route('/categories/<int:category_id>/courses/new', methods=['GET', 'POST'])
def new_course(category_id):
	if request.method == 'POST':
		new_course = Courses(name=request.form['name'], description=request.form[
						'description'], link=request.form['link'],photo_url=request.form['photo_url'], category_id=category_id)
		session.add(new_course)
		session.commit()

		return redirect(url_for('show_courses', category_id=category_id))
	else:
		return render_template('new_course.html', category_id=category_id)

@app.route('/categories/<int:category_id>/courses/<int:course_id>/edit/', methods=['GET', 'POST'])
def edit_course(category_id, course_id):
	edited_course=session.query(Courses).filter_by(id=course_id).one()
	if request.method == 'POST':
		if request.form['name']:
			edited_course.name = request.form['name']
		if request.form['description']:
			edited_course.description = request.form['description']
		if request.form['link']:
			edited_course.link = request.form['link']
		if request.form['photo_url']:
			edited_course.photo_url = request.form['photo_url']
			
		session.add(edited_course)
		session.commit()
		return redirect(url_for('show_courses', category_id=category_id))
	else:

		return render_template(
			'edit_course.html', category_id=category_id, course_id=course_id, course=edited_course)
	
@app.route('/categories/<int:category_id>/courses/<int:course_id>/delete/', methods=['GET', 'POST'])
def delete_course(category_id, course_id):
	deleted_course=session.query(Courses).filter_by(id=course_id).one()
	if request.method == 'POST':
		session.delete(deleted_course)
		session.commit()
		return redirect(url_for('show_courses', category_id=category_id))
	else:
		return render_template('delete_course.html',category_id=category_id,course=deleted_course)

@app.route('/categories/<int:category_id>/courses/<int:course_id>')
def course_details(category_id, course_id):
	course=session.query(Courses).filter_by(id=course_id).one()
	return render_template('course_details.html', category_id=category_id, course_id=course_id,course=course)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
