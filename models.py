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
        # Convert byte string to standard string
        hashed_utf8 = hashed_pwd.decode('utf-8')
        u = cls()
        u.username = username
        u.password = hashed_utf8
        u.email = email
        u.first_name = first_name
        u.last_name = last_name
        db.session.add(u)
        db.session.commit()

        if u:
            return u.username
        else:
            return False

    def login_user(self, password):
        print(self.password)
        print(password)
        valid = bcrypt.check_password_hash(self.password, password)
        if valid:
            return self.username
        else:
            return False
