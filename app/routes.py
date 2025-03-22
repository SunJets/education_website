import flask_jwt_extended.exceptions
from flask import url_for, request, redirect, flash, jsonify, get_flashed_messages
from app import app
import sqlalchemy as sa
from app import db
from app.models import User
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


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
        return jsonify(error=get_flashed_messages()), 400

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

    if not validate_username(username) and not validate_email(email):   # validate info
        flash('This user already exists')
        return jsonify(error=get_flashed_messages()), 400

    user = User(username=username, email=email)     # create a new user
    user.set_password(password)     # add and hash the password
    db.session.add(user)
    db.session.commit()

    return jsonify(username=user.username, email=user.email), 200


def validate_username(username):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is not None:
        return False

    return True


def validate_email(email):
    user = db.session.scalar(sa.select(User).where(User.email == email))
    if user is not None:
        return False

    return True