from flask import request, flash, jsonify, get_flashed_messages
from app import app
import sqlalchemy as sa
from app import db
from app.models import User, Course, CustomCourse
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


@app.route('/api/delete-course/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_course(id):
    username = get_jwt_identity()
    user = db.session.scalar(sa.select(User).where(User.username == username))

    if user is None:
        flash('User is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    course = db.session.scalar(user.courses.select().where(Course.id == id))

    if course is None:
        flash('Courses are not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    safe_delete_any_course(course)

    return jsonify(message='success'), 200


@app.route('/api/save-custom-courses', methods=['POST'])
@jwt_required()
def save_custom_courses():
    username = get_jwt_identity()
    user = db.session.scalar(sa.select(User).where(User.username == username))

    if user is None:
        flash('User is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    course_id = request.json.get('id')

    if course_id is None:
        flash('Course is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    course_id = int(course_id)
    courses_title = request.json.get('title')
    courses_description = request.json.get('description')

    add_custom_course_to_db(courses_title, courses_description, user.id, course_id)

    message = get_flashed_messages()
    if not message:
        message = 'success'
    return jsonify(message=message), 200


@app.route('/api/get-custom-course-names/<int:id>', methods=['GET'])    # get all custom course names with id
@jwt_required()
def get_custom_course_names(id):
    """
    this function and get_custom_course separated because it divides rendering names and rendering their body
    this is for better performance because the client's part will contain less content
    """

    username = get_jwt_identity()
    user = db.session.scalar(sa.select(User).where(User.username == username))

    if user is None:
        flash('User is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    custom_courses = create_custom_course_names_dict(user, id)

    if custom_courses is None:
        flash('Custom courses are not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    return jsonify(courses=custom_courses), 200


@app.route('/api/get-custom-course/<int:id>', methods=['GET'])      # get info about this custom course
@jwt_required()
def get_custom_course(id):
    """
    this function and get_custom_course_names separated because it divides rendering names and rendering their body
    this is for better performance because the client's part will contain less content
    """


    username = get_jwt_identity()
    user = db.session.scalar(sa.select(User).where(User.username == username))

    if user is None:
        flash('User is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    custom_course = db.session.scalar(sa.select(CustomCourse).where(CustomCourse.id == id))

    if custom_course is None:
        flash('Custom course is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    return jsonify(title=custom_course.title, description=custom_course.description), 200


@app.route('/api/delete-custom-course/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_custom_course(id):
    username = get_jwt_identity()
    user = db.session.scalar(sa.select(User).where(User.username == username))

    if user is None:
        flash('User is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    custom_course = db.session.scalar(user.custom_courses.select().where(CustomCourse.id == id))

    if custom_course is None:
        flash('Custom course is not found')
        return jsonify(error=get_flashed_messages()[0]), 400

    safe_delete_any_course(custom_course)

    return jsonify(message='success'), 200


@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    return jsonify(error="Unauthorized user"), 401

@jwt.invalid_token_loader
def invalid_token_response(error):
    return jsonify(error="Invalid token"), 422

@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    return jsonify(error="Expired token"), 401

@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):
    return jsonify(error="Revoked token"), 422


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


def add_custom_course_to_db(title, description, user_id, course_id):
        new_custom_course = CustomCourse(title=title, description=description, user_ref_id=user_id, course_ref_id=course_id)

        try:
            db.session.add(new_custom_course)
            db.session.commit()
        except:
            flash(f'''Custom course "{title}" wasn't added''')
            db.session.rollback()


def create_custom_course_names_dict(user, course_id):    # ONLY FOR ID AND NAME OF EACH CUSTOM COURSE
    custom_course_list = []
    custom_courses = db.session.scalars(user.custom_courses.select()).all()

    for course in custom_courses:
        course_dict = {'id': course_id, 'title': course.title}
        custom_course_list.append(course_dict)

    return custom_course_list


def safe_delete_any_course(course):      # change status of course or custom course to 0
    course.status = 0
    db.session.commit()


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

