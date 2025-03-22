import flask_jwt_extended.exceptions
from flask import url_for, request, redirect, flash, jsonify, get_flashed_messages
from app import app
import sqlalchemy as sa
from app import db
from app.models import User
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@app.route('/api/login', methods=['POST'])
def login():
    try:
        current_user = get_jwt_identity()
        if current_user:
            flash('You are already authorized')
            return jsonify(error=get_flashed_messages()), 400

    except NoAuthorizationError:
        pass

    username = request.json.get('username')
    password = request.json.get('password')

    user_request = sa.select(User).where(User.username == username)
    user = db.session.scalar(user_request)
    if user is None or not user.check_password(password):
        flash('Invalid username or password')
        return jsonify(error=get_flashed_messages()), 400

    token = create_access_token(identity=username)

    return jsonify(username=user.username, email=user.email, token=token), 200


@app.route('/api/register', methods=['POST'])
def register():
    try:
        current_user = get_jwt_identity()
        if current_user:
            return redirect(url_for('index'))

    except NoAuthorizationError:
        pass

    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if not validate_username(username) and not validate_email(email):
        flash('This user already exists')
        return jsonify(error=get_flashed_messages()), 400

    user = User(username=username, email=email)
    user.set_password(password)
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