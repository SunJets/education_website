import flask_jwt_extended.exceptions
from flask import url_for, request, redirect, flash, jsonify, get_flashed_messages
from app import app
import sqlalchemy as sa
from app import db
from app.models import User, Course
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re
from app import jwt


@app.route('/api/login', methods=['POST'])
@jwt_required(optional=True)
def login():
    current_user = get_jwt_identity()   # check if a user is authorized
    if current_user is not None:
        flash('You are already authorized')
        return jsonify(error=get_flashed_messages()), 400

    username = request.json.get('username')
    password = request.json.get('password')

    user_request = sa.select(User).where(User.username == username)
    user = db.session.scalar(user_request)    # get user from db
    if user is None or not user.check_password(password):   # check if user exists or his password is valid
        flash('Invalid username or password')
        return jsonify(error=get_flashed_messages()[0]), 400

    token = create_access_token(identity=username)

    return jsonify(username=user.username, email=user.email, token=token), 200


@app.route('/api/register', methods=['POST'])
@jwt_required(optional=True)
def register():
    current_user = get_jwt_identity()  # check if a user is authorized
    if current_user is not None:
        flash('You are already authorized')
        return jsonify(error=get_flashed_messages()), 400

    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if not validate_username(username) or not validate_email(email):   # validate info
        flash('This user already exists')
        return jsonify(error=get_flashed_messages()[0]), 400

    user = User(username=username, email=email)     # create a new user
    user.set_password(password)     # add and hash the password
    db.session.add(user)
    db.session.commit()

    return jsonify(username=user.username, email=user.email), 200


@app.route('/api/save-courses', methods=['POST'])
@jwt_required()
def save_courses():
    username = get_jwt_identity()
    user = db.session.scalar(sa.select(User).where(User.username == username))

    if user is None:
        flash('User is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    courses = request.json.get('courses')

    if courses is None:
        flash('Courses are not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    add_courses_to_db(courses, user.id)

    message = get_flashed_messages()
    if not message:
        message = 'success'
    return jsonify(message=message), 200


@app.route('/api/get-courses', methods=['GET'])
@jwt_required()
def get_courses():
    username = get_jwt_identity()
    user = db.session.scalar(sa.select(User).where(User.username == username))

    if user is None:
        flash('User is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    courses = create_courses_dict(user)

    if courses is None:
        flash('Courses are not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    return jsonify(courses=courses), 200


@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    return jsonify(error="Unauthorized user"), 401




def add_courses_to_db(course_list, user_id):
    for course in course_list:
        title = course['title']
        description = course['description']

        new_course = Course(title=title, description=description, user_ref_id=user_id)
        try:
            db.session.add(new_course)
            db.session.commit()
        except:
            flash(f'''Course "{title}" wasn't added''')
            db.session.rollback()


def create_courses_dict(user):
    course_list = []
    courses = db.session.scalars(user.courses.select()).all()

    for course in courses:
        course_dict = {'title': course.title, 'description': course.description}
        course_list.append(course_dict)

    return course_list



def validate_username(username):
    regex = r'^[A-Za-z0-9_]+$'
    if not re.fullmatch(regex, username):    # check if nickname has nothing except numbers, english letters
        return False                         # and underscore

    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is not None:
        return False

    return True


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex, email):  # check if email is written correctly
        return False

    user = db.session.scalar(sa.select(User).where(User.email == email))
    if user is not None:
        return False

    return True