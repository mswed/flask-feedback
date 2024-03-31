from flask import Flask, render_template, redirect, flash, session
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from utils import authorize


def create_app(database='feedback_db'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{database}'
    app.config['SECRET_KEY'] = 'whatever'
    connect_db(app)

    @app.route('/')
    def home():
        if 'username' in session:
            return redirect(f'/users/{session["username"]}')

        return redirect('/register')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if 'username' in session:
            return redirect(f'/users/{session["username"]}')

        form = RegisterForm()
        if form.validate_on_submit():
            u = User.register_user(form.username.data,
                                   form.password.data,
                                   form.email.data,
                                   form.first_name.data,
                                   form.last_name.data)
            if u:
                session['username'] = u
                return redirect(f'/users/{u}')

        return render_template('/register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'username' in session:
            return redirect(f'/users/{session["username"]}')
        
        form = LoginForm()
        if form.validate_on_submit():
            u = User.query.get_or_404(form.username.data)
            if u:
                u.authenticate(form.password.data)
                session['username'] = u.username
                print('Redirecting to', f'/users/{u.username}')
                return redirect(f'/users/{u.username}')

        return render_template('/login.html', form=form)

    @app.route('/users/<string:username>/delete', methods=['POST'])
    def delete_user(username):
        if authorize(username):
            u = User.query.filter_by(username=username).first()
            db.session.delete(u)
            db.session.commit()
            session.pop('username')

        return redirect('/')

    @app.route('/users/<string:username>')
    def show_secret(username):
        if authorize(username):
            u = User.query.get_or_404(username)
            return render_template('/secret.html', user=u)

        return redirect('/401')

    @app.route('/logout')
    def logout():
        session.pop('username')

        return redirect('/')

    @app.route('/users/<string:username>/feedback/add', methods=['GET', 'POST'])
    def add_feedback(username):
        if authorize(username):
            form = FeedbackForm()
            if form.validate_on_submit():
                f = Feedback()
                f.title = form.title.data
                f.content = form.content.data
                f.username = username
                db.session.add(f)
                db.session.commit()
                return redirect(f'/users/{username}')

            return render_template('/add_feedback.html', form=form)

        return redirect('/')

    @app.route('/feedback/<int:pid>/update', methods=['GET', 'POST'])
    def update_feedback(pid):
        feedback = Feedback.query.get_or_404(pid)
        username = feedback.username
        if authorize(username):
            form = FeedbackForm()

            if form.validate_on_submit():
                feedback.title = form.title.data
                feedback.content = form.content.data
                db.session.add(feedback)
                db.session.commit()
                return redirect(f'/users/{username}')
            else:
                form.title.data = feedback.title
                form.content.data = feedback.content
                return render_template('/edit_feedback.html', form=form)

        return redirect('/')

    @app.route('/feedback/<int:pid>/delete', methods=['POST'])
    def delete_feedback(pid):
        feedback = Feedback.query.get_or_404(pid)
        username = feedback.username
        if authorize(username):
            Feedback.query.filter_by(id=feedback.id).delete()
            db.session.commit()

        return redirect(f'/users/{username}')

    @app.errorhandler(404)
    def not_found(e):
        return render_template('/404.html')

    return app

