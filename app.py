from flask import Flask, render_template, redirect, flash, session
from models import connect_db, db, User
from forms import RegisterForm


def create_app(database='feedback_db'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{database}'
    app.config['SECRET_KEY'] = 'whatever'
    connect_db(app)

    @app.route('/')
    def home():
        return redirect('/register')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            u = User.register_user(form.username.data,
                                   form.password.data,
                                   form.email.data,
                                   form.first_name.data,
                                   form.last_name.data)
            if u:
                session['username'] = u
                return redirect('/secret')

        return render_template('/register.html', form=form)

    @app.route('/secret')
    def show_secret():
        return render_template('/secret.html')
    return app
