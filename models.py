from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """
    
    @param app: 
    @return: 
    """
    
    db.app = app
    db.init_app(app)


class User(db.Model):
    """
    User model
    @param username: text (20 characters), primary key
    @param password: text, user password hash
    @param email: text (50 characters), unique, user email
    @param first_name: text (30 characters), user's first name
    @param last_name: text (30 characters), user's _db name

    """
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register_user(cls, username, password, email, first_name, last_name):
        hashed_pwd = bcrypt.generate_password_hash(password)
        u = cls()
        u.username = username
        u.password = hashed_pwd
        u.email = email
        u.first_name = first_name
        u.last_name = last_name
        db.session.add(u)
        db.session.commit()

        if u:
            return u.username
        else:
            return False
