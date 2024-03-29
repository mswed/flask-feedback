from flask import Flask, render_template, redirect, flash
from models import connect_db, db, User


def create_app(database='feedback_db'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{database}'
    app.config['SECRET_KEY'] = 'whatever'
    connect_db(app)

    return app
