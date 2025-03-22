from flask import url_for, render_template, redirect, flash
from app import app

@app.route('/')
def index():
    return 'Hi'